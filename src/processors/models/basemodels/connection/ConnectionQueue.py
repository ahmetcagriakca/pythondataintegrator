from typing import List

from infrastructor.json.JsonConvert import JsonConvert
from models.basemodels.connection.ConnectionServer import ConnectionServer


@JsonConvert.register
class ConnectionQueue:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 Servers: List[ConnectionServer] = None,
                 Protocol: str = None,
                 Mechanism: str = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.Servers: List[ConnectionServer] = Servers
        self.Protocol: str = Protocol
        self.Mechanism: str = Mechanism
        self.User: str = User
        self.Password: str = Password
