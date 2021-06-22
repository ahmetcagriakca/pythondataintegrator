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

    def job_start(self, job_id, data_operation_id):
        conn = self.connect_rpc()
        job = conn.root.job_start(job_id, data_operation_id)
        return job