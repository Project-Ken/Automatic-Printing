from . import os
from . import json

class Config:
    def __new__(cls, path:str, default:dict):
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.isfile(path):
            with open(path, 'w', encoding='utf-8') as file:
                file.write(json.dump(default, indent=4))

        return super().__new__(cls)

    def __init__(self, path: str, default: dict):
        self.path = path
        self.default = default
        self.Load()

    def Load(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            for key, value in json.loads(file.read()).items():
                setattr(self, key, value)

    def Save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dump(self.__dict__.items(), indent=4))

    def Get(self, key:str, default=None):
        return getattr(self, key, default)
