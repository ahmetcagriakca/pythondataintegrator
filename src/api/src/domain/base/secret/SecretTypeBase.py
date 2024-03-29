from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from src.domain.base.secret.SecretBase import SecretBase


class SecretTypeBase(EntityBase):
    def __init__(self,
                 Name: str = None,
                 Secrets: List[SecretBase] = [],
                 AuthenticationTypes: List[AuthenticationTypeBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: int = Name
        self.Secrets = Secrets
        self.AuthenticationTypes = AuthenticationTypes
