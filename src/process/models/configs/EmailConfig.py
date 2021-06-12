from models.configs.BaseConfig import BaseConfig


class EmailConfig(BaseConfig):

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 user: str = None,
                 password: str = None,
                 from_addr:str=None
                 ):
        self.host:str = host
        self.port: str = port
        self.user: int = user
        self.password: str = password
        self.from_addr: str = from_addr

    def is_valid(self):
        pass
