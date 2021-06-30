from typing import List

from models.base.EntityBase import EntityBase
from models.base.integration.DataIntegrationColumnBase import DataIntegrationColumnBase
from models.base.integration.DataIntegrationConnectionBase import DataIntegrationConnectionBase
from models.base.operation.DataOperationIntegrationBase import DataOperationIntegrationBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataIntegrationBase(EntityBase):
    def __init__(self,
                 DefinitionId:int = None,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Definition = None,
                 Columns: List[DataIntegrationColumnBase] =[],
                 Connections: List[DataIntegrationConnectionBase] =[],
                 DataOperationIntegrations: List[DataOperationIntegrationBase] =[],
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
