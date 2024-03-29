from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.connection.ConnectionSecretBase import ConnectionSecretBase
from src.domain.base.secret.SecretSourceBase import SecretSourceBase


class SecretBase(EntityBase):
    def __init__(self,
                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType=None,
                 SecretSources: List[SecretSourceBase] = [],
                 ConnectionSecrets: List[ConnectionSecretBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
        self.SecretSources: List[SecretSourceBase] = SecretSources
        self.ConnectionSecrets: List[ConnectionSecretBase] = ConnectionSecrets
