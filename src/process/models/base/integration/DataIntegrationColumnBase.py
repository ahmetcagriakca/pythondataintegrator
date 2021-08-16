from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataIntegrationColumnBase(EntityBase):

    def __init__(self,
                 DataIntegrationId:int=None,
                 ResourceType: str = None,
                 SourceColumnName: str = None,
                 TargetColumnName: str = None,
                 DataIntegration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataIntegrationId = DataIntegrationId
        self.ResourceType: str = ResourceType
        self.SourceColumnName: str = SourceColumnName
        self.TargetColumnName: str = TargetColumnName
        self.DataIntegration = DataIntegration
