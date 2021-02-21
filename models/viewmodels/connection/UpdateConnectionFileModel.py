class UpdateConnectionFileModel:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.User: str = User
        self.Password: str = Password
