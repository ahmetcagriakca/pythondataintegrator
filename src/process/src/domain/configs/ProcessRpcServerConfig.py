from pdip.configuration.models.base import BaseConfig


class ProcessRpcServerConfig(BaseConfig):

    def __init__(self,
                 protocol_config: str = None,
                 port: int = None):
        self.protocol_config: str = protocol_config
        self.port: int = port

    def is_valid(self):
        pass
