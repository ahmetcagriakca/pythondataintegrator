import datetime
from dataclasses import dataclass
from typing import List

from infrastructor.json.JsonConvert import JsonConvert


@dataclass
class DataOperationContactDto:
    Id: int = None
    Email: str = None

    def to_dict(self):
        dic = self.__dict__
        return dic


@JsonConvert.register
@dataclass
class DataOperationListDto:
    Id: int = None
    Name: int = None
    Contacts: List[DataOperationContactDto] = None
    DefinitionId: int = None
    CreationDate: datetime.datetime = None
    LastUpdatedDate: datetime.datetime = None
    IsDeleted: int = None

    def to_dict(self):
        dic = self.__dict__
        dic["Contacts"] = [entity.to_dict() for entity in self.Contacts]
        return dic
