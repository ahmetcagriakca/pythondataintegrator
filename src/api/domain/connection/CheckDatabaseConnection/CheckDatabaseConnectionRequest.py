from dataclasses import dataclass

from domain.common.decorators.requestclass import requestclass
from infrastructure.cqrs.ICommand import ICommand

@requestclass
class CheckDatabaseConnectionRequest(ICommand):
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
