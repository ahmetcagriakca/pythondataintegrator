class PagingModifier:
    def __init__(self,
                 Id: int = None,
                 End: int = None,
                 Start: int = None,
                 Limit: int = None,
                 ):
        self.Id = Id
        self.Start = Start
        self.End = End
        self.Limit = Limit