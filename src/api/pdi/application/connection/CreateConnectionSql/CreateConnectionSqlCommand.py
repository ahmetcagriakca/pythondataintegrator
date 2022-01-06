from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.connection.CreateConnectionSql.CreateConnectionSqlRequest import \
    CreateConnectionSqlRequest


@dataclass
class CreateConnectionSqlCommand(ICommand):
    request: CreateConnectionSqlRequest = None
