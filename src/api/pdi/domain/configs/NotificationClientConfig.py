from pdip.configuration.models.base import BaseConfig


class NotificationClientConfig(BaseConfig):

    def __init__(self,
                 host: str = None,
                 port: int = None):
        self.host: str = host
        self.port: int = port

    def is_valid(self):
        pass
