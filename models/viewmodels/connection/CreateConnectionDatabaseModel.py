class CreateConnectionDatabaseModel:
    def __init__(self,
                 Name: str = None,
                 ConnectionTypeName: int = None,
                 ConnectorTypeName: int = None,
                 Host: str = None,
                 Port: int = None,
                 Sid: str = None,
                 DatabaseName: str = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Name: str = Name
        self.ConnectionTypeName: str = ConnectionTypeName
        self.ConnectorTypeName: str = ConnectorTypeName
        self.Host: str = Host
        self.Port: int = Port
        self.Sid: str = Sid
        self.DatabaseName: str = DatabaseName
        self.User: str = User
        self.Password: str = Password
