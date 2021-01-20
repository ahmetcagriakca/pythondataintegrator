from models.viewmodels.integration.UpdateDataIntegrationModel import UpdateDataIntegrationModel


class UpdateDataOperationIntegrationModel:
    def __init__(self,
                 Limit: int = None,
                 ProcessCount: int = None,
                 Integration: UpdateDataIntegrationModel = None,
                 *args, **kwargs):
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.Integration: UpdateDataIntegrationModel = Integration