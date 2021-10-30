from typing import List

from pdip.data import EntityBase

from pdi.domain.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from pdi.domain.base.secret.SecretBase import SecretBase


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
