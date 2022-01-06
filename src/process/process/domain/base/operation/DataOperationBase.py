from typing import List

from pdip.data.domain import EntityBase

from process.domain.base.operation.DataOperationContactBase import DataOperationContactBase
from process.domain.base.operation.DataOperationIntegrationBase import DataOperationIntegrationBase
from process.domain.base.operation.DataOperationJobBase import DataOperationJobBase


class DataOperationBase(EntityBase):
    def __init__(self,
                 DefinitionId: int = None,
                 Name: str = None,
                 Definition=None,
                 DataOperationJobs: List[DataOperationJobBase] = [],
                 Integrations: List[DataOperationIntegrationBase] = [],
                 Contacts: List[DataOperationContactBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Contacts = Contacts
        self.Integrations = Integrations
        self.DataOperationJobs = DataOperationJobs
        self.DefinitionId: int = DefinitionId
        self.Name: str = Name
        self.Definition = Definition
