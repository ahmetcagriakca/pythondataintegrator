class CreateDataOperationIntegrationModel:
    def __init__(self,
                 Code: str = None,
                 Order: str = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        self.Code: str = Code
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount