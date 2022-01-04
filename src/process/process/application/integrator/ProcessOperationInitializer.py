from injector import inject
from pdip.integrator.operation.base import OperationInitializer
from pdip.integrator.operation.domain import OperationBase
from pdip.logging.loggers.console import ConsoleLogger


class ProcessOperationInitializer(OperationInitializer):
    @inject
    def __init__(self, logger: ConsoleLogger):
        self.logger = logger

    def initialize(self, operation: OperationBase):
        self.logger.info('operation initialize:' + operation.Name)
        operation.Execution.Id = 1500
