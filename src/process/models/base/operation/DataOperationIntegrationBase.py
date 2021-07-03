from typing import List
from models.base.EntityBase import EntityBase
from models.base.operation.DataOperationJobExecutionIntegrationBase import DataOperationJobExecutionIntegrationBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataOperationIntegrationBase(EntityBase):

    def __init__(self,
                 DataOperationId: int = None,
                 DataIntegrationId: int = None,
                 Order: int = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 DataOperation=None,
                 DataIntegration=None,
                 DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegrationBase]=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrations = DataOperationJobExecutionIntegrations
        self.DataOperationId: int = DataOperationId
        self.DataIntegrationId: int = DataIntegrationId
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.DataOperation = DataOperation
        self.DataIntegration = DataIntegration
