import rpyc
from rpyc.utils.server import ThreadedServer

from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from domain.connection.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest
from domain.connection.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountCommand import \
    CheckDatabaseTableRowCountCommand
from domain.connection.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountRequest import \
    CheckDatabaseTableRowCountRequest
from infrastructure.cqrs.Dispatcher import Dispatcher
from models.configs.ProcessRpcServerConfig import ProcessRpcServerConfig
from rpc.OperationProcess import OperationProcess


class ProcessService(rpyc.Service):
    def __init__(self):
        pass

    def initialize(self, process_rpc_server_config: ProcessRpcServerConfig):
        protocol_config = process_rpc_server_config.protocol_config  # {'allow_public_attrs': True, 'sync_request_timeout': 60}
        server = ThreadedServer(ProcessService, port=process_rpc_server_config.port, protocol_config=protocol_config)
        try:
            server.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            pass

    def exposed_job_start(self, data_operation_id=None, job_id=None, data_operation_job_execution_id=None, *args,
                          **kwargs):
        operation_process = OperationProcess()
        result = operation_process.start_operation_process(data_operation_id=data_operation_id, job_id=job_id,
                                                           data_operation_job_execution_id=data_operation_job_execution_id)
        del operation_process
        return result

    def exposed_check_database_connection(self, connection_name=None, *args, **kwargs):
        dispatcher: Dispatcher = Dispatcher()
        req = CheckDatabaseConnectionRequest(ConnectionName=connection_name)
        check_database_connection_command = CheckDatabaseConnectionCommand(
            request=req)
        dispatcher.dispatch(check_database_connection_command)

    def exposed_check_database_table_row_count(self, connection_name=None, schema=None, table=None, *args, **kwargs):
        dispatcher: Dispatcher = Dispatcher()
        req = CheckDatabaseTableRowCountRequest(ConnectionName=connection_name, Schema=schema, Table=table)
        check_database_count_command = CheckDatabaseTableRowCountCommand(
            request=req)
        dispatcher.dispatch(check_database_count_command)
