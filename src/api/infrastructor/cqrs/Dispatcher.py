from typing import Type, TypeVar

from injector import inject

from IocManager import IocManager
from infrastructor.cqrs.CommandQueryBase import CommandQueryBase
from infrastructor.cqrs.ICommand import ICommand
from infrastructor.cqrs.ICommandHandler import ICommandHandler
from infrastructor.cqrs.IQuery import IQuery
from infrastructor.cqrs.IQueryHandler import IQueryHandler
from infrastructor.dependency.scopes import IScoped

T = TypeVar('T', covariant=True)


class Dispatcher(IScoped):
    @inject
    def __init__(self):
        pass

    def find_handler(self, type, handler_type: Type[T]) -> T:
        for handler_class in handler_type.__subclasses__():
            result = handler_type[type] == handler_class.__orig_bases__[0]
            if result:
                instance = IocManager.injector.get(handler_class)
                return instance

    def dispatch(self, cq: CommandQueryBase[T]) -> T:
        if isinstance(cq, IQuery):
            handler_type = IQueryHandler
        elif isinstance(cq, ICommand):
            handler_type = ICommandHandler
        handler = self.find_handler(cq.__class__, handler_type)
        if handler is None:
            raise Exception("Handler not founded")
        return handler.handle(cq)
