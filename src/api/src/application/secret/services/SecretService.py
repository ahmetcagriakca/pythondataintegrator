from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from src.application.secret.services.SecretSourceService import SecretSourceService
from src.application.secret.services.SecretTypeService import SecretTypeService
from src.domain.dto.ConnectionBasicAuthentication import ConnectionBasicAuthentication
from src.domain.enums import SecretTypes
from src.domain.secret import Secret


class SecretService(IScoped):

    @inject
    def __init__(self,
                 secret_type_service: SecretTypeService,
                 secret_source_service: SecretSourceService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.secret_repository = repository_provider.get(Secret)
        self.secret_type_service = secret_type_service
        self.secret_source_service = secret_source_service

    def create_secret(self, name: str, type_id: str) -> Secret:
        secret_type = self.secret_type_service.get_by_id(id=type_id)
        secret = Secret(Name=name, SecretType=secret_type)
        return secret

    def get_basic_authentication(self, id: str) -> ConnectionBasicAuthentication:
        """
        Create File connection
        """
        secret = self.secret_repository.first(IsDeleted=0, Id=id)
        connection_basic_authentication = self.secret_source_service.get_basic_authentication(secret=secret)
        return connection_basic_authentication

    def create_basic_authentication(self, name: str, user: str, password: str) -> Secret:
        """
        Create File connection
        """
        secret = self.create_secret(name=name, type_id=SecretTypes.Source.value)
        self.secret_source_service.create_basic_authentication(secret=secret, user=user, password=password)
        return secret

    def update_basic_authentication(self, id: int, user: str, password: str) -> Secret:
        """
        Create File connection
        """
        secret = self.secret_repository.first(IsDeleted=0, Id=id)
        if secret is None:
            raise OperationalException("Secret Not Found")
        else:
            self.secret_source_service.update_basic_authentication(secret=secret, user=user, password=password)
        return secret

    def create_kerberos_authentication(self, name: str, principal: str, password: str, krb_realm: str, krb_fqdn: str,
                                       krb_service_name: str) -> Secret:
        """
        Create File connection
        """
        secret = self.create_secret(name=name, type_id=SecretTypes.Source.value)
        self.secret_source_service.create_kerberos_authentication(
            secret=secret,
            principal=principal,
            password=password,
            krb_realm=krb_realm,
            krb_fqdn=krb_fqdn,
            krb_service_name=krb_service_name
        )
        return secret

    def update_kerberos_authentication(self, id: int, principal: str, password: str, krb_realm: str, krb_fqdn: str,
                                       krb_service_name: str) -> Secret:
        """
        Create File connection
        """
        secret = self.secret_repository.first(IsDeleted=0, Id=id)
        if secret is None:
            raise OperationalException("Secret Not Found")
        else:
            self.secret_source_service.update_kerberos_authentication(
                secret=secret,
                principal=principal,
                password=password,
                krb_realm=krb_realm,
                krb_fqdn=krb_fqdn,
                krb_service_name=krb_service_name
            )
        return secret

    def delete_secret(self, id: int):
        """
        Delete secret
        """
        secret = self.secret_repository.first(Id=id, IsDeleted=0)
        if secret is None:
            raise OperationalException("Secret Not Found")

        self.secret_repository.delete_by_id(secret.Id)
        if secret.SecretSources is not None:
            for secret_source in secret.SecretSources:
                self.secret_source_service.delete(id=secret_source.Id)
