from pdip.cqrs.decorators import requestclass
from pdip.integrator.operation.domain import OperationBase


@requestclass
class ExecuteOperationFinishRequest:
    Operation: OperationBase = None
    Exception: Exception = None
