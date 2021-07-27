from domain.common.decorators.requestclass import requestclass


@requestclass
class GetDataOperationRequest:
    Id: int = None
