from injector import inject
from pdip.integrator.integration.base import OperationIntegrationInitializer
from pdip.integrator.operation.domain import OperationIntegrationBase
from pdip.logging.loggers.console import ConsoleLogger


class ProcessOperationIntegrationInitializer(OperationIntegrationInitializer):
    @inject
    def __init__(self, logger: ConsoleLogger):
        self.logger = logger

    def initialize(self, operation_integration: OperationIntegrationBase):
        self.logger.info('operation_integration initialize:' + operation_integration.Name)
        operation_integration.Execution.Id = 1550
