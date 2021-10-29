from pdip.data import EntityBase


class DefinitionBase(EntityBase):

    def __init__(self,
                 Name: str = None,
                 Version: int = None,
                 Content: str = None,
                 IsActive: bool = None,
                 DataOperations=[],
                 DataIntegrations=[],
                 DataOperationJobExecutions=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutions = DataOperationJobExecutions
        self.DataIntegrations = DataIntegrations
        self.DataOperations = DataOperations
        self.Name: str = Name
        self.Version: int = Version
        self.Content: str = Content
        self.IsActive: bool = IsActive
