from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationBase


@requestclass
class ExecuteOperationInitializeRequest:
    Operation: OperationBase = None
