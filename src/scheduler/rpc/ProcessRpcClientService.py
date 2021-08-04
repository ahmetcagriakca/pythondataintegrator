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

    def call_job_start(self, data_operation_id, job_id, data_operation_job_execution_id):
        conn = self.connect_rpc()
        job = conn.root.job_start(data_operation_id, job_id, data_operation_job_execution_id)
        return job
