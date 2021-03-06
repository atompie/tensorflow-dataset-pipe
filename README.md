# tensorflow-dataset-pipe

If you are having problems with data preparation for keras model this library may help.

Suppose you have a csv fie with data you would like to train on. 

## Example of csv file

```csv
    Product title, Category
    Addias shoes, 1
    Nike sneakers, 1
    Wireless router, 2
    ....
```

Your input date is in the first column and output data is in the 2nd column.
You need to encode both input and output. YOu could start like this:

```python
from dataset_pipe.feeds.datasets import XYDataset


dataset = XYDataset("csv")
data = dataset.feed("file.csv")

# x is your input
# y is your output

for x, y in data:
    print(x)

```

Run this and you will see:

```bash
OrderedDict([('input', "Addias shoes"), OrderedDict([('output', 1)])
```

This way you can debug if the library is reading the right data.

## Filtering and mapping

Now lest map and filter (optionally) the data. Mapping is necessary for the encoding process.
 
```
from dataset_pipe.feeds.datasets import XYDataset

def mapper(data):
    words = data[0].split()     # split first column into words
    
    if len(words)==1:           # filter short title descriptions
        return None

    category = int(data[1])     # return category as int
    return                      # return tuple of input and output
        {'x': words},           # input
        {'y': category}         # output


dataset = XYDataset("csv")
data = dataset.map(mapper).feed("file.csv")
for x, y in data:
    print(x, y)

```

If you ran this you should see an ordered dictionary of input and outpu data. 
Input should be splitted into words

## Encoding

In order to encode data you need an Encoder. Encoder is a class thats implements EncoderInterface.


This is an example of OneHotEncoder. Encoder needs 4 methods. 

* encode - this is where the data will be encoded
* shape - this method returns the shape of the encoded vector
* type - this method returns the tensorflow data type (tf.dtype) of encoded vector
* dim - returns dimension of the vector

```python
from dataset_pipe.encoders.math.ops import zeros


class OneHotEncoder:

    def __init__(self, dim):
        self._dim = dim
        self._shape = (dim,)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, int):
            raise ValueError("Param data must be integer. {} given fo type {}".format(data, type(data)))

        """
        Data  is a list of category ids, e.g. 12
        Return dense one hot encoded vector
        """
        vector = zeros(self._shape)
        vector[data] = 1.0
        return vector

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim

```

Basic encoders are included in the library so you do not have to write it on your own.
OneHotEncoder is also included in the library. Now will use this encoder together with DictToBinaryEncoder to 
encode mapped data.

```python
from dataset_pipe.feeds.datasets import XYDataset
from dataset_pipe.encoders.dict_to_binary_encoder import DictToBinaryEncoder
from dataset_pipe.encoders.one_hot_encoder import OneHotEncoder


def mapper(data):
    words = data[0].split()     # split first column into words
    
    if len(words)==1:           # filter short title descriptions
        return None

    category = int(data[1])     # return category as int
    
    # return tuple of input and output
    return {'x': words}, {'y': category}     

bag_of_words_2_idx = {
    "addidas": 1,
    "nike": 2
}


dataset = XYDataset("csv")
dataset.map(mapper)
dataset.encode(
    {"x": DictToBinaryEncoder(bag_of_words_2_idx)}, 
    {"y": OneHotEncoder(10)})


for x, y in dataset.feed("file.csv").batch(10):
    print(x, y)

```

If your model requires more the one input or output map it this way:

```python
def mapper(data):
    x1 = data[0].split()
    x2 = data[1]
    y1 = int(data[2])    
    y2 = list(data[3])

    # return tuple of input and output
    return {'x1': x1, 'x2': x2}, {'y1': y1, 'y2': y2} 
```

And encode it this way:

```python
dataset.encode(
    {"x1": DictToBinaryEncoder(bag_of_words_2_idx), "x1": OneHotEncoder(10)}, 
    {"y1": OneHotEncoder(10), 'y2': BinaryEncoder(10)})
```

Remember order maters when maping and encoding.  

```python
train_dataset = dataset.feed("train.csv").batch(10)  # pass it to fit_generator method in keras
eval_dataset = dataset.feed("eval.csv").batch(10)

...

model.fit_generator(
            train_dataset,
            validation_data=eval_dataset,
            steps_per_epoch=10,
            validation_steps=5,
            epochs=10
)
```