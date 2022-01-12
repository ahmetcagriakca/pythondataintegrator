from pdip.cqrs.decorators import requestclass


@requestclass
class GetConnectionBigDataRequest:
    Id: int = None
