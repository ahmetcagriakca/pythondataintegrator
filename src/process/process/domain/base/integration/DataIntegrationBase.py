from typing import List

from pdip.data.domain import EntityBase

from process.domain.base.integration.DataIntegrationColumnBase import DataIntegrationColumnBase
from process.domain.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase


class DataIntegrationBase(EntityBase):
    def __init__(self,
                 DefinitionId: int = None,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Definition=None,
                 Columns: List[DataIntegrationColumnBase] = [],
                 Connections: List[DataIntegrationConnectionBase] = [],
                 DataOperationIntegrations = [],
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
