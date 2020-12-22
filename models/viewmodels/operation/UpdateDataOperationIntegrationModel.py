class UpdateDataOperationIntegrationModel:
    def __init__(self,
                 Id:int=None,
                 Code: str = None,
                 Order: str = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        self.Id: str = Id
        self.Code: str = Code
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount