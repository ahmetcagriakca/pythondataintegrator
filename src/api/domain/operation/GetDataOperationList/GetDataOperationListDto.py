import datetime
from typing import List

from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class DataOperationContactDto:
    Id: int = None
    Email: str = None


@dtoclass
class GetDataOperationListDto:
    Id: int = None
    Name: str = None
    Contacts: List[DataOperationContactDto] = None
    DefinitionId: int = None
    CreationDate: datetime.datetime = None
    LastUpdatedDate: datetime.datetime = None
    IsDeleted: int = None
