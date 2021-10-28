from injector import inject
from pdip.dependency import IScoped
from pdip.exceptions import IncompatibleAdapterException

from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationLimitOff import \
    ExecuteIntegrationLimitOff
from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationProcess import \
    ExecuteIntegrationProcess
from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationSerial import ExecuteIntegrationSerial
from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationStrategy import \
    ExecuteIntegrationStrategy
from domain.operation.execution.services.OperationCacheService import OperationCacheService


class ExecuteIntegrationStrategyFactory(IScoped):
    @inject
    def __init__(self,
                 operation_cache_service: OperationCacheService,
                 execute_integration_limit_off: ExecuteIntegrationLimitOff,
                 execute_integration_process: ExecuteIntegrationProcess,
                 execute_integration_serial: ExecuteIntegrationSerial,
                 ):
        self.execute_integration_serial = execute_integration_serial
        self.execute_integration_process = execute_integration_process
        self.execute_integration_limit_off = execute_integration_limit_off
        self.operation_cache_service = operation_cache_service

    def get(self, data_operation_integration_id) -> ExecuteIntegrationStrategy:
        # Source and target database managers instantiate
        data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(
            data_operation_integration_id=data_operation_integration_id)
        # only target query run
        if data_operation_integration.Limit is None or data_operation_integration.Limit == 0:
            if isinstance(self.execute_integration_limit_off, ExecuteIntegrationStrategy):
                return self.execute_integration_limit_off
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_integration_limit_off} is incompatible with {ExecuteIntegrationStrategy}")
        elif data_operation_integration.ProcessCount is not None and data_operation_integration.ProcessCount > 1:
            if isinstance(self.execute_integration_process, ExecuteIntegrationStrategy):
                return self.execute_integration_process
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_integration_adapter} is incompatible with {ExecuteIntegrationStrategy}")
        else:
            if isinstance(self.execute_integration_serial, ExecuteIntegrationStrategy):
                return self.execute_integration_serial
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_integration_serial} is incompatible with {ExecuteIntegrationStrategy}")
