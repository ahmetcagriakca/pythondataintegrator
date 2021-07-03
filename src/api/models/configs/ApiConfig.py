from models.configs.BaseConfig import BaseConfig


class ApiConfig(BaseConfig):

    def __init__(self,
                 is_debug: bool = None,
                 port: int = None,
                 origins: str = None):
        self.port: int = port
        self.is_debug: bool = is_debug
        self.origins: str = origins

    def is_valid(self):
        pass
