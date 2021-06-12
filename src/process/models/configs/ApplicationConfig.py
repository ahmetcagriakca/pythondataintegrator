from models.configs.BaseConfig import BaseConfig


class ApplicationConfig(BaseConfig):

    def __init__(self,
                 api_node: bool = None,
                 process_node: bool = None,):
        self.api_node: bool = api_node
        self.process_node: bool = process_node

    def is_valid(self):
        pass
