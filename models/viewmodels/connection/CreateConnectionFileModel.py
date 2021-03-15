from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class CreateConnectionFileModel:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 Folder: str = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Folder = Folder
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.User: str = User
        self.Password: str = Password
