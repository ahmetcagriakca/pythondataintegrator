from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class SecretSourceBasicAuthenticationBase(EntityBase):
    def __init__(self,
                 SecretSourceId: int = None,
                 User: str = None,
                 Password: str = None,
                 SecretSource = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretSourceId: int = SecretSourceId
        self.User: str = User
        self.Password: str = Password
        self.SecretSource = SecretSource
