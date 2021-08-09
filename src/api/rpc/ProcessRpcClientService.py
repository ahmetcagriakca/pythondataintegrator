import rpyc
from injector import inject
from infrastructure.dependency.scopes import IScoped
from models.configs.ProcessRpcClientConfig import ProcessRpcClientConfig


class ProcessRpcClientService(IScoped):

    @inject
    def __init__(self,
                 process_rpc_client_config: ProcessRpcClientConfig,
                 ):
        self.process_rpc_client_config = process_rpc_client_config

    def connect_rpc(self):
        conn = rpyc.connect(self.process_rpc_client_config.host, self.process_rpc_client_config.port)
        conn._config['timeout'] = 240
        conn.ASYNC_REQUEST_TIMEOUT = 240
        conn._config['sync_request_timeout'] = 240  # Set timeout to 240 seconds
        return conn

    def call_check_database_connection(self, connection_name=None, *args, **kwargs):
        conn = self.connect_rpc()
        result = conn.root.check_database_connection(connection_name)
        return result

    def call_check_database_table_row_count(self, connection_name=None, schema=None, table=None, *args, **kwargs):
        conn = self.connect_rpc()
        result = conn.root.check_database_table_row_count(connection_name, schema, table)
        return result
