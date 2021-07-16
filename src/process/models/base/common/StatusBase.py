from typing import List

from models.base.EntityBase import EntityBase
from models.base.operation import DataOperationJobExecutionBase
from models.base.operation.DataOperationJobExecutionIntegrationBase import DataOperationJobExecutionIntegrationBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class StatusBase(EntityBase):
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Description: bool = None,
                 DataOperationJobExecutions: List[DataOperationJobExecutionBase]  = [],
                 DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegrationBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: str = Id
        self.Name: str = Name
        self.Description: bool = Description
        self.DataOperationJobExecutionIntegrations = DataOperationJobExecutionIntegrations
        self.DataOperationJobExecutions = DataOperationJobExecutions
