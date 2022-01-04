from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationIntegrationBase


@requestclass
class ExecuteOperationIntegrationTargetTruncateRequest:
    OperationIntegration: OperationIntegrationBase = None
    RowCount: str = None
