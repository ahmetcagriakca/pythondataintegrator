
from typing import List
from models.base.secret.SecretSourceBase import SecretSourceBase
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class AuthenticationTypeBase(EntityBase):
    def __init__(self,
    
                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType = None,
                 SecretSources: List[SecretSourceBase]=[],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
        self.SecretSources = SecretSources
