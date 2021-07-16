from typing import Generic, TypeVar

from infrastructor.cqrs.CommandQueryHandlerBase import CommandQueryHandlerBase
from infrastructor.cqrs.ICommand import ICommand

CH = TypeVar('CH', covariant=True, bound=ICommand)


class ICommandHandler(Generic[CH], CommandQueryHandlerBase[CH]):
    def __init__(self) -> CH:
        pass

    def handle(self, query: CH) -> CH:
        pass