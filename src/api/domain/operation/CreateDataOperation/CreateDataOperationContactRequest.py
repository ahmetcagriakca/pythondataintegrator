from domain.common.decorators.requestclass import requestclass


@requestclass
class CreateDataOperationContactRequest:
    Email: str = None
