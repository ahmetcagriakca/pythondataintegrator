from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.data.seed import Seed
from pdip.logging.loggers.sql import SqlLogger

from pdi.domain.common import ConfigParameter


class ConfigParameterSeed(Seed):
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
            config_parameter_repository = self.repository_provider.get(ConfigParameter)
            check_count = config_parameter_repository.table.count()
            if check_count is None or check_count == 0:
                configurations = [
                    {
                        "Name": "EMAIL_HOST",
                        "Type": "str",
                        "Value": "",
                        "Description": "Email Host Address"
                    },
                    {
                        "Name": "EMAIL_PORT",
                        "Type": "int",
                        "Value": "",
                        "Description": "Email Port"
                    },
                    {
                        "Name": "EMAIL_FROM",
                        "Type": "str",
                        "Value": "",
                        "Description": "Email From"
                    },
                    {
                        "Name": "EMAIL_SMTP",
                        "Type": "str",
                        "Value": "",
                        "Description": "Email From"
                    },
                    {
                        "Name": "EMAIL_USER",
                        "Type": "str",
                        "Value": "",
                        "Description": "Email User"
                    },
                    {
                        "Name": "EMAIL_PASSWORD",
                        "Type": "str",
                        "Value": "",
                        "Description": "Email User"
                    },
                    {
                        "Name": "DataOperationDefaultContact",
                        "Type": "str",
                        "Value": "",
                        "Description": "default mail user"
                    }
                ]
                for configJson in configurations:
                    config_parameter = ConfigParameter(Name=configJson["Name"], Type=configJson["Type"],
                                                       Value=configJson["Value"], Description=configJson["Description"])
                    config_parameter_repository.insert(config_parameter)
                    self.repository_provider.commit()
        except Exception as ex:
            self.logger.exception(ex, "ApScheduler seeds getting error")
