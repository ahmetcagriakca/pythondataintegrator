from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationBase


@requestclass
class ExecuteOperationStartRequest:
    Operation: OperationBase = None
