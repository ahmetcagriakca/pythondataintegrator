from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class ConnectionDatabase:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 Host: str = None,
                 Port: int = None,
                 Sid: str = None,
                 ServiceName: str = None,
                 DatabaseName: str = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.Host: str = Host
        self.Port: int = Port
        self.Sid: str = Sid
        self.ServiceName: str = ServiceName
        self.DatabaseName: str = DatabaseName
        self.User: str = User
        self.Password: str = Password
