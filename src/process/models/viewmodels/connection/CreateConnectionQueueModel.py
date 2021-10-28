from typing import List

from pdip.json import JsonConvert
from models.viewmodels.connection.CreateConnectionServerModel import CreateConnectionServerModel


@JsonConvert.register
class CreateConnectionQueueModel:
    def __init__(self,
                 Name: str = None,
                 ConnectorTypeName: int = None,
                 Servers: List[CreateConnectionServerModel] = None,
                 Protocol: str = None,
                 Mechanism: str = None,
                 User: str = None,
                 Password: str = None,
                 ):
        self.Name: str = Name
        self.ConnectorTypeName: str = ConnectorTypeName
        self.Servers: List[CreateConnectionServerModel] = Servers
        self.Protocol: str = Protocol
        self.Mechanism: str = Mechanism
        self.User: str = User
        self.Password: str = Password
