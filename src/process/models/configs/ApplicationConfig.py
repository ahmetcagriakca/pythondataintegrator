from models.configs.BaseConfig import BaseConfig


class ApplicationConfig(BaseConfig):

    def __init__(self,
                 root_directory: str = None,
                 environment: str = None,
                 name: str = None,
                 secret_key: str = None,
                 ):
        self.root_directory: str = root_directory
        self.name: str = name
        self.environment: str = environment
        self.secret_key = secret_key

    def is_valid(self):
        pass
