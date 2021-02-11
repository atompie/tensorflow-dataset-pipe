from interface import Interface


class EncoderInterface(Interface):

    def encode(self, data):
        pass

    def shape(self):
        pass

    def type(self):
        pass

    def dim(self):
        pass