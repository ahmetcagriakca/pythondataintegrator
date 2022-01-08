from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.operation.DataOperationJobExecutionIntegrationBase import \
    DataOperationJobExecutionIntegrationBase


class DataOperationIntegrationBase(EntityBase):

    def __init__(self,
                 DataOperationId: int = None,
                 DataIntegrationId: int = None,
                 Order: int = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 DataOperation=None,
                 DataIntegration=None,
                 DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegrationBase] = [],
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
