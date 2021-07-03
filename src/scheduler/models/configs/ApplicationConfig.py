from models.configs.BaseConfig import BaseConfig


class ApplicationConfig(BaseConfig):

    def __init__(self,
                 root_directory: str = None,
                 name: str = None,
                 environment: str = None,
                 hostname: str = None,
                 secret_key: str = None,
                 ):
        self.root_directory: str = root_directory
        self.name: str = name
        self.environment: str = environment
        self.hostname = hostname
        self.secret_key = secret_key

    def is_valid(self):
        pass
