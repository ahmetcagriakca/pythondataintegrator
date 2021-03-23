
class DataQueueTask:
    def __init__(self,
                 Data: any = None,
                 IsFinished: bool = False,
                 IsProcessed: bool = False,
                 Message: str = None,
                 Exception: Exception = None,


                 ):
        self.Data: any = Data
        self.IsFinished: bool = IsFinished
        self.IsProcessed: bool = IsProcessed
        self.Message: str = Message
        self.Exception: Exception = Exception