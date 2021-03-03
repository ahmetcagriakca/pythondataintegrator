# This decorator will check unexpected database error for thread operations
def transaction_handler(func):
    def inner(*args, **kwargs):
        try:
            args[0].database_session_manager.connect()
            result= func(*args, **kwargs)
            args[0].database_session_manager.commit()
            # args[0].database_session_manager.close()
            return result
        except Exception as ex:
            args[0].database_session_manager.rollback()
            args[0].database_session_manager.connect()
            print(ex)
            raise

    return inner
