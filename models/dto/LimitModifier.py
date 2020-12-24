from infrastructor.multi_processing.ParallelMultiProcessing import ProcessBaseData


class LimitModifier(ProcessBaseData):
    def __init__(self,
                 Id: int = None,
                 TopLimit: int = None,
                 SubLimit: int = None,
                 ):
        super().__init__(Id)
        self.SubLimit = SubLimit
        self.TopLimit = TopLimit