class Info:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Base:
    def __init__(self, info:Info):
        self.info = info
        self.connection = None

    def __new__(cls, *args, **kwargs):
        if cls is Base:
            raise TypeError('Base Class Cannot be Instantiated Directly')
        return super().__new__(cls)
