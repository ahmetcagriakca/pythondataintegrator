from pdip.data import EntityBase


class ConnectionSecretBase(EntityBase):

    def __init__(self,
                 ConnectionId: int = None,
                 SecretId: int = None,
                 Connection=None,
                 Secret=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: int = ConnectionId
        self.SecretId: int = SecretId
        self.Connection = Connection
        self.Secret = Secret
