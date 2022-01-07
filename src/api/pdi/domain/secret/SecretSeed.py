from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.data.seed import Seed
from pdip.integrator.connection.domain.authentication.type import AuthenticationTypes
from pdip.logging.loggers.sql import SqlLogger

from pdi.domain.enums import SecretTypes
from pdi.domain.secret import SecretType, AuthenticationType


class SecretSeed(Seed):
    @inject
    def __init__(
            self,
            repository_provider: RepositoryProvider,
            logger: SqlLogger,
    ):
        self.logger = logger
        self.repository_provider = repository_provider

    def seed(self):
        try:
            secret_type_repository = self.repository_provider.get(SecretType)
            check_count = secret_type_repository.table.count()
            if check_count is None or check_count == 0:

                secret_type_list = [
                    {
                        "Name": SecretTypes.Source.name,
                    },
                ]
                for secret_type_json in secret_type_list:
                    secret_type = SecretType(Name=secret_type_json["Name"])
                    secret_type_repository.insert(secret_type)
                    self.repository_provider.commit()

            authentication_type_repository = self.repository_provider.get(AuthenticationType)
            check_count = authentication_type_repository.table.count()
            if check_count is None or check_count == 0:
                authentication_type_list = [
                    {
                        "SecretType": SecretTypes.Source.name,
                        "Name": AuthenticationTypes.BasicAuthentication.name,
                    },
                    {
                        "SecretType": SecretTypes.Source.name,
                        "Name": AuthenticationTypes.Kerberos.name,
                    },
                ]
                for authentication_type_json in authentication_type_list:
                    secret_type = secret_type_repository.filter_by(
                        Name=authentication_type_json["SecretType"]).first()
                    authentication_type = AuthenticationType(Name=authentication_type_json["Name"],
                                                             SecretType=secret_type)
                    authentication_type_repository.insert(authentication_type)
                    self.repository_provider.commit()
        except Exception as ex:
            self.logger.exception(ex, f"ApScheduler seeds getting error")
        finally:
            self.repository_provider.close()
