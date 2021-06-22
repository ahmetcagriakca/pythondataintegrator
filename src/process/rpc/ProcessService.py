import rpyc
from rpyc.utils.server import ThreadedServer

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

    def exposed_job_start(self, job_id, data_operation_id, *args, **kwargs):
        return OperationProcess.start_operation_process(data_operation_id=data_operation_id, job_id=job_id)
