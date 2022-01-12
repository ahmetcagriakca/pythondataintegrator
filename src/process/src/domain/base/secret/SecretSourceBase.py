from typing import List

from pdip.data.domain import EntityBase

from src.domain.base.secret.SecretSourceBasicAuthenticationBase import SecretSourceBasicAuthenticationBase
from src.domain.base.secret.SecretSourceKerberosAuthenticationBase import SecretSourceKerberosAuthenticationBase


class SecretSourceBase(EntityBase):
    def __init__(self,
                 SecretId: int = None,
                 AuthenticationTypeId: int = None,
                 Secret=None,
                 AuthenticationType=None,
                 SecretSourceBasicAuthentications: List[SecretSourceBasicAuthenticationBase] = [],
                 SecretSourceKerberosAuthentications: List[SecretSourceKerberosAuthenticationBase] = [],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretId: int = SecretId
        self.AuthenticationTypeId: int = AuthenticationTypeId
        self.Secret = Secret
        self.AuthenticationType = AuthenticationType
        self.SecretSourceBasicAuthentications: List[
            SecretSourceBasicAuthenticationBase] = SecretSourceBasicAuthentications
        self.SecretSourceKerberosAuthentications: List[
            SecretSourceKerberosAuthenticationBase] = SecretSourceKerberosAuthentications
