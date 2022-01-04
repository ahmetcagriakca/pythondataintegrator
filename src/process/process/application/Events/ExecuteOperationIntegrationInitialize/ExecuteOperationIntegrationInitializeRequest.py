from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationIntegrationBase


@requestclass
class ExecuteOperationIntegrationInitializeRequest:
    OperationIntegration: OperationIntegrationBase = None
    Message: str = None
