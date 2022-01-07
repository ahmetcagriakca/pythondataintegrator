from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.integrator.connection.domain.authentication.type import AuthenticationTypes

from pdi.application.secret.services.AuthenticationTypeService import AuthenticationTypeService
from pdi.application.secret.services.SecretSourceBasicAuthenticationService import \
    SecretSourceBasicAuthenticationService
from pdi.application.secret.services.SecretSourceKerberosAuthenticationService import \
    SecretSourceKerberosAuthenticationService
from pdi.domain.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication
from pdi.domain.secret import Secret, SecretSource


class SecretSourceService(IScoped):

    @inject
    def __init__(self,
                 authentication_type_service: AuthenticationTypeService,
                 secret_source_basic_authentication_service: SecretSourceBasicAuthenticationService,
                 secret_source_kerberos_authentication_service: SecretSourceKerberosAuthenticationService,
                 repository_provider: RepositoryProvider,
                 ):
        self.secret_source_kerberos_authentication_service = secret_source_kerberos_authentication_service
        self.repository_provider = repository_provider
        self.secret_source_repository = repository_provider.get(SecretSource)
        self.secret_source_basic_authentication_service = secret_source_basic_authentication_service
        self.authentication_type_service = authentication_type_service

    def create_secret_source(self, secret: Secret, authentication_type_id):
        authentication_type = self.authentication_type_service.get_by_id(
            id=authentication_type_id)
        secret_source = SecretSource(AuthenticationType=authentication_type, Secret=secret)
        self.secret_source_repository.insert(secret_source)
        return secret_source

    def get_basic_authentication(self, secret: Secret) -> ConnectionBasicAuthentication:
        """
        Create File connection
        """
        secret_source = self.secret_source_repository.first(IsDeleted=0, Secret=secret)
        connection_basic_authentication = self.secret_source_basic_authentication_service.get_by_secret_source(
            secret_source=secret_source)
        return connection_basic_authentication

    def create_basic_authentication(self, secret: Secret, user: str, password: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.create_secret_source(authentication_type_id=AuthenticationTypes.BasicAuthentication.value,
                                                  secret=secret)
        self.secret_source_basic_authentication_service.create(secret_source=secret_source, user=user,
                                                               password=password)
        return secret_source

    def update_basic_authentication(self, secret: Secret, user: str, password: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.secret_source_repository.first(IsDeleted=0, Secret=secret)
        if secret_source is None:
            raise OperationalException("Secret Source Not Found")
        self.secret_source_basic_authentication_service.update(secret_source=secret_source, user=user,
                                                               password=password)
        return secret_source

    def create_kerberos_authentication(self, secret: Secret, principal: str, password: str, krb_realm: str,
                                       krb_fqdn: str, krb_service_name: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.create_secret_source(authentication_type_id=AuthenticationTypes.Kerberos.value,
                                                  secret=secret)
        self.secret_source_kerberos_authentication_service.create(
            secret_source=secret_source,
            principal=principal,
            password=password,
            krb_realm=krb_realm,
            krb_fqdn=krb_fqdn,
            krb_service_name=krb_service_name
        )
        return secret_source

    def update_kerberos_authentication(self, secret: Secret, principal: str, password: str, krb_realm: str,
                                       krb_fqdn: str, krb_service_name: str) -> SecretSource:
        """
        Create File connection
        """
        secret_source = self.secret_source_repository.first(IsDeleted=0, Secret=secret)
        if secret_source is None:
            raise OperationalException("Secret Source Not Found")
        self.secret_source_kerberos_authentication_service.update(
            secret_source=secret_source,
            principal=principal,
            password=password,
            krb_realm=krb_realm,
            krb_fqdn=krb_fqdn,
            krb_service_name=krb_service_name
        )
        return secret_source

    def delete(self, id: int):
        """
        Delete Secret Source
        """
        secret_source = self.secret_source_repository.first(Id=id, IsDeleted=0)
        if secret_source is None:
            raise OperationalException("Secret Source Not Found")

        self.secret_source_repository.delete_by_id(secret_source.Id)
        if secret_source.SecretSourceBasicAuthentications is not None:
            for secret_source_basic_authentication in secret_source.SecretSourceBasicAuthentications:
                self.secret_source_basic_authentication_service.delete(id=secret_source_basic_authentication.Id)
        if secret_source.SecretSourceKerberosAuthentications is not None:
            for secret_source_kerberos_authentication in secret_source.SecretSourceKerberosAuthentications:
                self.secret_source_kerberos_authentication_service.delete(id=secret_source_kerberos_authentication.Id)
