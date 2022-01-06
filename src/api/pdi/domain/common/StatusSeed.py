from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.data.seed import Seed
from pdip.logging.loggers.sql import SqlLogger

from pdi.domain.common import Status


class StatusSeed(Seed):
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
            status_repository = self.repository_provider.get(Status)
            check_count = status_repository.table.count()
            if check_count is None or check_count == 0:
                status_list = [
                    {
                        "Id": 1,
                        "Name": "Initialized",
                        "Description": "Initialized",
                    },
                    {
                        "Id": 2,
                        "Name": "Start",
                        "Description": "Start",
                    },
                    {
                        "Id": 3,
                        "Name": "Finish",
                        "Description": "Finish",
                    },
                    {
                        "Id": 4,
                        "Name": "Error",
                        "Description": "Error",
                    },
                ]
                statuses = []
                for status_json in status_list:
                    status = Status(
                        Name=status_json["Name"],
                        Description=status_json["Description"]
                    )
                    status_repository.insert(status)
                    self.repository_provider.commit()
        except Exception as ex:
            self.logger.exception(ex, "ApScheduler seeds getting error")
