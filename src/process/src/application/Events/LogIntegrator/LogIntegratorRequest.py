from pdip.cqrs.decorators import requestclass


@requestclass
class LogIntegratorRequest:
    Data: any = None
    Message: str = None
    Exception: Exception = None
