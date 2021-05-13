from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class ConnectionServer:
    def __init__(self,
                 Host: str = None,
                 Port: int = None,
                 ):
        self.Host: str = Host
        self.Port: int = Port
