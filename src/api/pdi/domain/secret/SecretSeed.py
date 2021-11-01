from pdip.data import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.database import SqlLogger

from pdip.data import Seed
from pdi.domain.enums import SecretTypes, AuthenticationTypes
from pdi.domain.secret import SecretType, AuthenticationType


class SecretSeed(Seed):
    def seed(self):
        try:
            repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
            secret_type_repository = repository_provider.get(SecretType)
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
                    repository_provider.commit()

            authentication_type_repository = repository_provider.get(AuthenticationType)
            check_count = authentication_type_repository.table.count()
            if check_count is None or check_count == 0:
                authentication_type_list = [
                    {
                        "SecretType": SecretTypes.Source.name,
                        "Name": AuthenticationTypes.BasicAuthentication.name,
                    },
                ]
                for authentication_type_json in authentication_type_list:
                    secret_type = secret_type_repository.filter_by(
                        Name=authentication_type_json["SecretType"]).first()
                    authentication_type = AuthenticationType(Name=authentication_type_json["Name"],
                                                             SecretType=secret_type)
                    authentication_type_repository.insert(authentication_type)
                    repository_provider.commit()
        except Exception as ex:
            logger = DependencyContainer.Instance.get(SqlLogger)
            logger.exception(ex, f"ApScheduler seeds getting error")
        finally:
            repository_provider.close()
