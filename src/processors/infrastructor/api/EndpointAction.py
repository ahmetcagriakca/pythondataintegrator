class EndpointAction:
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        response = self.action(**kwargs)
        return response
