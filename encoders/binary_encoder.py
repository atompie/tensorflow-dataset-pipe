from encoders.interfaces.encoder_interface import EncoderInterface
from interface import implements
from encoders.math.ops import zeros
import numpy as np


class BinaryEncoder(implements(EncoderInterface)):

    def __init__(self, dim, repeat_output=0):
        self.repeat_output = repeat_output
        self._dim = dim
        self._shape = (dim,)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, list):
            raise ValueError("Param data must be list. {} given fo type {}".format(data, type(data)))

        vector = zeros(self._shape)
        for bit in data:
            vector[bit] = 1.0

        if self.repeat_output > 0:
            return np.repeat(np.array([vector]), self.repeat_output, axis=0)
        return vector

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim


if __name__ == "__main__":
    wae = BinaryEncoder(dim=10, repeat_output=2)
    a = wae.encode([0, 1, 2, 9])
    print(a)
    print(a.shape)
