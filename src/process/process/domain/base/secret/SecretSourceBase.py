from typing import List

from pdip.data.domain import EntityBase

from process.domain.base.secret.SecretSourceBasicAuthenticationBase import SecretSourceBasicAuthenticationBase


class SecretSourceBase(EntityBase):
    def __init__(self,
                 SecretId: int = None,
                 AuthenticationTypeId: int = None,
                 Secret=None,
                 AuthenticationType=None,
                 SecretSourceBasicAuthentications: List[SecretSourceBasicAuthenticationBase] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretId: int = SecretId
        self.AuthenticationTypeId: int = AuthenticationTypeId
        self.Secret = Secret
        self.AuthenticationType = AuthenticationType
        self.SecretSourceBasicAuthentications: List[
            SecretSourceBasicAuthenticationBase] = SecretSourceBasicAuthentications
