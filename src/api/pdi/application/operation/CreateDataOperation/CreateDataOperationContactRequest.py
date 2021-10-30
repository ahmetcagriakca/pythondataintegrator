from pdip.cqrs.decorators import requestclass


@requestclass
class CreateDataOperationContactRequest:
    Email: str = None
