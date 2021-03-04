# This decorator will check unexpected database error for thread operations
import gc


def transaction_handler(func):
    def inner(*args, **kwargs):
        try:
            args[0].database_session_manager.connect()
            result= func(*args, **kwargs)
            args[0].database_session_manager.commit()
            gc.collect()
            # args[0].database_session_manager.close()
            return result
        except Exception as ex:
            args[0].database_session_manager.rollback()
            args[0].database_session_manager.close()
            gc.collect()
            print(ex)
            raise

    return inner
