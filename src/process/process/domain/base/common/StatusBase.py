from typing import List

from pdip.data import EntityBase

from process.domain.base.operation import DataOperationJobExecutionBase
from process.domain.base.operation.DataOperationJobExecutionIntegrationBase import DataOperationJobExecutionIntegrationBase


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
