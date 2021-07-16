from typing import List

from models.base.secret.SecretBase import SecretBase
from models.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class SecretTypeBase(EntityBase):
    def __init__(self,
                 Name: int = None,
                 Secrets: List[SecretBase] = None,
                 AuthenticationTypes: List[AuthenticationTypeBase] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: int = Name
        self.Secrets: List[SecretBase] = Secrets
        self.AuthenticationTypes: List[AuthenticationTypeBase] = AuthenticationTypes
