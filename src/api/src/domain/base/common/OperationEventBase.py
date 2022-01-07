from pdip.data.domain import EntityBase


class OperationEventBase(EntityBase):

    def __init__(self,
                 Code: int = None,
                 Name: str = None,
                 Description: str = None,
                 Class: str = None,
                 DataOperationJobExecutionEvents=[],
                 DataOperationJobExecutionIntegrationEvents=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrationEvents = DataOperationJobExecutionIntegrationEvents
        self.DataOperationJobExecutionEvents = DataOperationJobExecutionEvents
        self.Code: int = Code
        self.Name: str = Name
        self.Description: str = Description
        self.Class: str = Class
