from models.configs.BaseConfig import BaseConfig


class SchedulerRpcServerConfig(BaseConfig):

    def __init__(self,
                 protocol_config: str = None,
                 port: int = None):
        self.protocol_config: str = protocol_config
        self.port: int = port

    def is_valid(self):
        pass
