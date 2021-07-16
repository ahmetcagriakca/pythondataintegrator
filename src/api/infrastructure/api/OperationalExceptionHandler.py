import traceback

from IocManager import IocManager
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.exceptions.OperationalException import OperationalException
from infrastructure.logging.SqlLogger import SqlLogger


@IocManager.api.errorhandler(OperationalException)
def handle_operational_exception(exception):
    separator = '|'
    default_content_type = "application/json"
    mime_type_string = "mimetype"
    """Return JSON instead of HTML for HTTP errors."""
    IocManager.injector.get(RepositoryProvider).rollback()
    # start with the correct headers and status code from the error
    exception_traceback = traceback.format_exc()
    output = separator.join(exception.args)
    output_message = "empty"
    if output is not None and output != "":
        output_message = output
    trace_message = "empty"
    if exception_traceback is not None and exception_traceback != "":
        trace_message = exception_traceback
    IocManager.injector.get(SqlLogger).error(f'Operational Exception Messsage:{output_message} - Trace:{trace_message}')
    return {
               "result": "",
               "isSuccess": "false",
               "message": output
           }, 400, {mime_type_string: default_content_type}