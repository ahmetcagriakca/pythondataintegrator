from injector import inject
from pdip.cqrs import ICommandHandler
from pdip.data.decorators import transactionhandler
from rpyc import connect

from src.application.StartProcess.StartProcessCommand import StartProcessCommand
from src.domain.configs.ProcessRpcClientConfig import ProcessRpcClientConfig


class StartProcessCommandHandler(ICommandHandler[StartProcessCommand]):
    @inject
    def __init__(self,
                 process_rpc_client_config: ProcessRpcClientConfig,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_rpc_client_config = process_rpc_client_config

    def connect_rpc(self):
        conn = connect(self.process_rpc_client_config.host, self.process_rpc_client_config.port)
        conn._config['timeout'] = 240
        conn.ASYNC_REQUEST_TIMEOUT = 240
        conn._config['sync_request_timeout'] = 240  # Set timeout to 240 seconds
        return conn

    def handle(self, command: StartProcessCommand):
        """
        :param command: command
        :return:
        """
        conn = self.connect_rpc()
        conn.root.job_start(command.DataOperationId, command.JobId, command.DataOperationJobExecutionId)
