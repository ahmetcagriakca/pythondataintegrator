class DataQueueTask:
    def __init__(self,
                 Id:int=None,
                 Data: any = None,
                 Start: int = None,
                 End: int = None,
                 Limit: int = None,
                 State: int = None,
                 IsFinished: bool = None,
                 IsProcessed: bool = None,
                 Traceback: str = None,
                 Exception: Exception = None,

                 ):
        self.Id = Id
        self.Start = Start
        self.End = End
        self.Limit = Limit
        self.Data: any = Data
        self.State: bool = State
        self.IsFinished: bool = IsFinished
        self.IsProcessed: bool = IsProcessed
        self.Traceback: str = Traceback
        self.Exception: Exception = Exception
