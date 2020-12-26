from models.configs.BaseConfig import BaseConfig


class DatabaseConfig(BaseConfig):

    def __init__(self,
                 type: str = None,
                 connection_string: str = None,
                 driver: str = None,
                 host: str = None,
                 port: int = None,
                 database: str = None,
                 username: str = None,
                 password: str = None,
                 ):
        self.connection_string = connection_string
        self.type = type
        self.driver: str = driver
        self.host: str = host
        self.port: int = port
        self.database: str = database
        self.username: str = username
        self.password: str = password

    def is_valid(self):
        pass
