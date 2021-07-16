from typing import Generic, TypeVar

from infrastructor.cqrs.IQuery import IQuery
from infrastructor.cqrs.CommandQueryHandlerBase import CommandQueryHandlerBase

QH = TypeVar('QH', covariant=True, bound=IQuery)


class IQueryHandler(Generic[QH], CommandQueryHandlerBase[QH]):
    def __init__(self) -> QH:
        pass

    def handle(self, query: QH) -> any:
        pass