from injector import inject
from pdip.base import Pdi
from pdip.cqrs import Dispatcher
from pdip.dependency import ISingleton
from pdip.dependency.container import DependencyContainer
from rpyc import Service
from rpyc.utils.server import ThreadedServer

from process.application.CheckDatabaseConnection.CheckDatabaseConnectionCommand import CheckDatabaseConnectionCommand
from process.application.CheckDatabaseConnection.CheckDatabaseConnectionRequest import CheckDatabaseConnectionRequest
from process.application.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountCommand import \
    CheckDatabaseTableRowCountCommand
from process.application.CheckDatabaseTableRowCount.CheckDatabaseTableRowCountRequest import \
    CheckDatabaseTableRowCountRequest
from process.domain.configs.ProcessRpcServerConfig import ProcessRpcServerConfig
from process.rpc.OperationProcess import OperationProcess


class ProcessService(Service, ISingleton):
    @inject
    def __init__(self):
        self.process_rpc_server_config = DependencyContainer.Instance.get(ProcessRpcServerConfig)


    def run(self):
        server = ThreadedServer(ProcessService, port=self.process_rpc_server_config.port,
                                protocol_config=self.process_rpc_server_config.protocol_config)
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
        dispatcher: Dispatcher = Pdi().get(Dispatcher)

        req = CheckDatabaseConnectionRequest(ConnectionName=connection_name)
        check_database_connection_command = CheckDatabaseConnectionCommand(
            request=req)
        dispatcher.dispatch(check_database_connection_command)

    def exposed_check_database_table_row_count(self, connection_name=None, schema=None, table=None, *args, **kwargs):
        dispatcher: Dispatcher = Pdi().get(Dispatcher)
        req = CheckDatabaseTableRowCountRequest(ConnectionName=connection_name, Schema=schema, Table=table)
        check_database_count_command = CheckDatabaseTableRowCountCommand(
            request=req)
        dispatcher.dispatch(check_database_count_command)
