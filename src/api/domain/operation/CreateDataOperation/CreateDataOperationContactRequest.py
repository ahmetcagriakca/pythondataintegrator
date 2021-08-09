from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CreateDataOperationContactRequest:
    Email: str = None
