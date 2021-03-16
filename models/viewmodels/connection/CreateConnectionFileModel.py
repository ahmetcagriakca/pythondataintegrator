from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class CreateConnectionFileModel:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 Host: str = None,
                 Port: int = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Host: str = Host
        self.Port: int = Port
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.User: str = User
        self.Password: str = Password
