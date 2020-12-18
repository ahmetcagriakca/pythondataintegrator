from models.configs.BaseConfig import BaseConfig


class PdiConfig(BaseConfig):

    def __init__(self,
                 limit: int = None,
                 process_count: int = None,
                 do_parallel: bool = None):
        self.limit: int = limit
        self.process_count: int = process_count
        self.do_parallel: bool  = do_parallel

    def is_valid(self):
        pass
