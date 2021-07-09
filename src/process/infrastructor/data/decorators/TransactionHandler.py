# This decorator will check unexpected database error for thread operations
from IocManager import IocManager
from infrastructor.data.RepositoryProvider import RepositoryProvider


def transaction_handler(func):
    def inner(*args, **kwargs):
        repository_provider = IocManager.injector.get(RepositoryProvider)
        try:
            result = func(*args, **kwargs)
            repository_provider.commit()
            return result
        except Exception as ex:
            repository_provider.rollback()
            print(ex)
            raise
        finally:
            repository_provider.close()

    return inner
