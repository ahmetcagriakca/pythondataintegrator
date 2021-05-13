# This decorator will check unexpected database error for thread operations
from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager


def transaction_handler(func):
    def inner(*args, **kwargs):
        database_session_manager = IocManager.injector.get(DatabaseSessionManager)
        try:
            result = func(*args, **kwargs)
            database_session_manager.commit()
            return result
        except Exception as ex:
            database_session_manager.rollback()
            print(ex)
            raise

    return inner
