from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dto.PagingModifier import PagingModifier


class ConnectionBasicAuthentication:
    def __init__(self,
                 User: str = None,
                 Password: str = None,
                 ):
        self.User: str = User
        self.Password: str = Password
