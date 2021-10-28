from typing import List

from pdip.data import EntityBase

from models.base.connection.ConnectionSecretBase import ConnectionSecretBase
from models.base.secret.SecretSourceBase import SecretSourceBase


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
