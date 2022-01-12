from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.operation import DataOperationJobExecutionBase
from src.domain.base.operation.DataOperationJobExecutionIntegrationBase import \
    DataOperationJobExecutionIntegrationBase


class StatusBase(EntityBase):
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Description: bool = None,
                 DataOperationJobExecutions: List[DataOperationJobExecutionBase] = [],
                 DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegrationBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: str = Id
        self.Name: str = Name
        self.Description: bool = Description
        self.DataOperationJobExecutionIntegrations = DataOperationJobExecutionIntegrations
        self.DataOperationJobExecutions = DataOperationJobExecutions
