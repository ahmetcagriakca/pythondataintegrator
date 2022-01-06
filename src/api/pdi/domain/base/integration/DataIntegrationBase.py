from typing import List

from pdip.data.domain import EntityBase

from pdi.domain.base.integration.DataIntegrationColumnBase import DataIntegrationColumnBase
from pdi.domain.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase
from pdi.domain.base.operation.DataOperationIntegrationBase import DataOperationIntegrationBase


class DataIntegrationBase(EntityBase):
    def __init__(self,
                 DefinitionId: int = None,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Definition=None,
                 Columns: List[DataIntegrationColumnBase] = [],
                 Connections: List[DataIntegrationConnectionBase] = [],
                 DataOperationIntegrations: List[DataOperationIntegrationBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationIntegrations = DataOperationIntegrations
        self.Connections = Connections
        self.Columns = Columns
        self.DefinitionId: int = DefinitionId
        self.Code: str = Code
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Definition = Definition
