class TaskBaseData:
    def __init__(self,
                 Id: int = None):
        self.Id: int = Id
        self.State: int = None
        self.Result = None
        self.Message: str = None
        self.Exception: Exception = None
        self.Traceback: Exception = None