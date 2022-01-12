from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationIntegrationBase


@requestclass
class ExecuteOperationIntegrationSourceRequest:
    OperationIntegration: OperationIntegrationBase = None
    RowCount: str = None
