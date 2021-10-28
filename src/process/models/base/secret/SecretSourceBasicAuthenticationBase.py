from pdip.data import EntityBase


class SecretSourceBasicAuthenticationBase(EntityBase):
    def __init__(self,
                 SecretSourceId: int = None,
                 User: str = None,
                 Password: str = None,
                 SecretSource=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretSourceId: int = SecretSourceId
        self.User: str = User
        self.Password: str = Password
        self.SecretSource = SecretSource
