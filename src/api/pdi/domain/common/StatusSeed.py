from pdip.data import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.database import SqlLogger

from pdip.data import Seed
from pdi.domain.common import Status


class StatusSeed(Seed):
    def seed(self):
        try:
            repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
            status_repository = repository_provider.get(Status)
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
                    repository_provider.commit()
        except Exception as ex:
            logger = DependencyContainer.Instance.get(SqlLogger)
            logger.exception(ex, "ApScheduler seeds getting error")
        finally:
            repository_provider.close()
