from infrastructor.multi_processing.models.TaskBaseData import TaskBaseData


class TaskData:
    def __init__(self,
                 Data: TaskBaseData = None,
                 SubProcessId: int = None,
                 IsFinished: bool = False,
                 IsProcessed: bool = False):
        self.Data: TaskBaseData = Data
        self.SubProcessId: int = SubProcessId
        self.IsFinished: bool = IsFinished
        self.IsProcessed: bool = IsProcessed