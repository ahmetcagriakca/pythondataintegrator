from models.configs.BaseConfig import BaseConfig


class ApsConfig(BaseConfig):
    def __init__(self,
                 coalesce: bool = None,
                 max_instances: str = None,
                 thread_pool_executer_count: bool = None,
                 process_pool_executer_count: int = None
                 ):
        self.process_pool_executer_count = process_pool_executer_count
        self.thread_pool_executer_count = thread_pool_executer_count
        self.max_instances = max_instances
        self.coalesce = coalesce

    def is_valid(self):
        pass
