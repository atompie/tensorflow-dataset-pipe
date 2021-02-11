import types
from interface import implements

from dataset_pipe.dataset import Dataset
from dataset_pipe.encoder_list import EncoderList
from encoders.interfaces.encoder_interface import EncoderInterface


class Generator:

    def __init__(self, data, input_encoders: EncoderList, output_encoders: EncoderList):
        if not isinstance(data, types.GeneratorType):
            raise ValueError("Data param is not generator")
        if not isinstance(input_encoders, EncoderList) and input_encoders is not None:
            raise ValueError("Param input_encoders must be EncoderList or None")
        if not isinstance(output_encoders, EncoderList) and output_encoders is not None:
            raise ValueError("Param output_encoders must be EncoderList or None")
        self._data = data
        if input_encoders:
            self._validate(input_encoders, 'input_encoders')
        if output_encoders:
            self._validate(output_encoders, 'output_encoders')
        self._input_encoders = input_encoders
        self._output_encoders = output_encoders

    def __iter__(self):
        if self._input_encoders and self._output_encoders:
            for x, y in self._data:
                x = self._input_encoders.encode(x)
                y = self._output_encoders.encode(y)
                yield tuple(x), tuple(y)
        else:
            for x, y in self._data:
                yield x, y

    def batch(self, *args, **kwargs):
        return self.__iter__()

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    @staticmethod
    def _validate(data, param_name):
        if not isinstance(data, dict):
            raise ValueError(f'Param {param_name} must be dict.')
        for name, encoder in data.items():
            if not isinstance(encoder, implements(EncoderInterface)):
                raise ValueError(
                    f'Encoder {param_name}.{name} must contain Encoders only that implement EncoderInterface.')

    def shapes(self):
        if self._output_encoders and self._input_encoders:
            return self._input_encoders.shapes(), self._output_encoders.shapes()
        return None, None

    def types(self):
        if self._output_encoders and self._input_encoders:
            return self._input_encoders.types(), self._output_encoders.types()
        return 'string', 'string'

    def dataset(self):
        return Dataset(self)
