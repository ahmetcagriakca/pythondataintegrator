from pdip.data.domain import EntityBase

class SecretSourceKerberosAuthenticationBase(EntityBase):
    def __init__(self,
                 SecretSourceId: int = None,
                 Principal: str = None,
                 Password: str = None,
                 KrbRealm: str = None,
                 KrbFqdn: str = None,
                 KrbServiceName: str = None,
                 SecretSource=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretSourceId: int = SecretSourceId
        self.Principal: str = Principal
        self.Password: str = Password
        self.KrbRealm: str = KrbRealm
        self.KrbFqdn: str = KrbFqdn
        self.KrbServiceName: str = KrbServiceName
        self.SecretSource = SecretSource
