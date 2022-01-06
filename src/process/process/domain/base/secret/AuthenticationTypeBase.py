from typing import List

from pdip.data.domain import EntityBase

from process.domain.base.secret.SecretSourceBase import SecretSourceBase


class AuthenticationTypeBase(EntityBase):
    def __init__(self,

                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType=None,
                 SecretSources: List[SecretSourceBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
        self.SecretSources = SecretSources
