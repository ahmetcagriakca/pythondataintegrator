
class LimitModifier:
    def __init__(self,
                 top_limit: int = None,
                 sub_limit: int = None,
                 ):
        self.sub_limit = sub_limit
        self.top_limit = top_limit