import rpyc
from injector import inject
from infrastructor.dependency.scopes import IScoped
from models.configs.ProcessRpcClientConfig import ProcessRpcClientConfig


class ProcessRpcClientService(IScoped):

    @inject
    def __init__(self,
                 process_rpc_client_config: ProcessRpcClientConfig,
                 ):
        self.process_rpc_client_config = process_rpc_client_config

    def connect_rpc(self):
        conn = rpyc.connect(self.process_rpc_client_config.host, self.process_rpc_client_config.port)
        return conn

    def call_job_start(self, data_operation_id,job_id,data_operation_job_execution_id ):
        conn = self.connect_rpc()
        job = conn.root.job_start(data_operation_id,job_id, data_operation_job_execution_id)
        return job