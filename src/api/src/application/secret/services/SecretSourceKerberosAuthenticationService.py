from injector import inject
from pdip.cryptography import CryptoService
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from src.domain.dto.ConnectionKerberosAuthentication import ConnectionKerberosAuthentication
from src.domain.secret import SecretSource
from src.domain.secret.SecretSourceKerberosAuthentication import SecretSourceKerberosAuthentication


class SecretSourceKerberosAuthenticationService(IScoped):

    @inject
    def __init__(self,
                 crypto_service: CryptoService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_source_kerberos_authentication_repository = repository_provider.get(
            SecretSourceKerberosAuthentication)
        self.crypto_service = crypto_service

    def get_by_secret_source(self, secret_source: SecretSource) -> ConnectionKerberosAuthentication:
        secret_source_kerberos_authentication = self.secret_source_kerberos_authentication_repository.first(
            IsDeleted=0, SecretSource=secret_source)
        connection_kerberos_authentication = ConnectionKerberosAuthentication(
            Principal=self.crypto_service.decrypt(secret_source_kerberos_authentication.User),
            Password=self.crypto_service.decrypt(secret_source_kerberos_authentication.Password)
        )

        return connection_kerberos_authentication

    def create(self, secret_source: SecretSource, principal: str, password: str, krb_realm: str, krb_fqdn: str,
               krb_service_name: str) -> SecretSourceKerberosAuthentication:
        """
        Create SecretSourceKerberosAuthentication
        """

        secret_source_kerberos_authentication = SecretSourceKerberosAuthentication(
            Principal=self.crypto_service.encrypt(principal),
            Password=self.crypto_service.encrypt(password),
            KrbRealm=krb_realm,
            KrbFqdn=krb_fqdn,
            KrbServiceName=krb_service_name,
            SecretSource=secret_source
        )
        self.secret_source_kerberos_authentication_repository.insert(secret_source_kerberos_authentication)
        return secret_source

    def update(self, secret_source: SecretSource, principal: str, password: str, krb_realm: str, krb_fqdn: str,
               krb_service_name: str) -> SecretSourceKerberosAuthentication:
        """
        Update SecretSourceKerberosAuthentication
        """
        secret_source_kerberos_authentication = self.secret_source_kerberos_authentication_repository.first(
            IsDeleted=0, SecretSource=secret_source)
        if secret_source_kerberos_authentication is None:
            raise OperationalException("Secret Source Kerberos Authentication Not Found")
        secret_source_kerberos_authentication.Principal = self.crypto_service.encrypt(principal)
        secret_source_kerberos_authentication.Password = self.crypto_service.encrypt(password)
        secret_source_kerberos_authentication.KrbRealm = krb_realm
        secret_source_kerberos_authentication.KrbFqdn = krb_fqdn
        secret_source_kerberos_authentication.KrbServiceName = krb_service_name

        return secret_source

    def delete(self, id: int):
        """
        Delete SecretSourceKerberosAuthentication
        """
        secret_source_kerberos_authentication = self.secret_source_kerberos_authentication_repository.first(Id=id,
                                                                                                            IsDeleted=0)
        if secret_source_kerberos_authentication is None:
            raise OperationalException("Secret Source Kerberos Authentication Not Found")

        self.secret_source_kerberos_authentication_repository.delete_by_id(secret_source_kerberos_authentication.Id)
