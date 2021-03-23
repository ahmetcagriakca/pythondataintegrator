from infrastructor.multi_processing.models.TaskBaseData import TaskBaseData


class PagingModifier(TaskBaseData):
    def __init__(self,
                 Id: int = None,
                 End: int = None,
                 Start: int = None,
                 Limit: int = None,
                 ):
        super().__init__(Id)
        self.Start = Start
        self.End = End
        self.Limit = Limit