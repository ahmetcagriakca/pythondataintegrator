from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationIntegrationBase


@requestclass
class ExecuteOperationIntegrationFinishRequest:
    OperationIntegration: OperationIntegrationBase = None
    Message: str = None
    Exception: Exception = None
