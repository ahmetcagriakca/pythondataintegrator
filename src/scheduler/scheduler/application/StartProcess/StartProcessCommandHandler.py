from injector import inject
from pdip.configuration.models.database import DatabaseConfig
from pdip.configuration.services import ConfigService
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.decorators import transactionhandler
from pdip.delivery import EmailProvider
from pdip.logging.loggers.sql import SqlLogger
from pdip.configuration.models.application import ApplicationConfig
from rpyc import connect

from scheduler.application.StartProcess.StartProcessCommand import StartProcessCommand
from scheduler.domain.configs.ProcessRpcClientConfig import ProcessRpcClientConfig


class StartProcessCommandHandler(ICommandHandler[StartProcessCommand]):
    @inject
    def __init__(self,
                 process_rpc_client_config: ProcessRpcClientConfig,
                 database_config: DatabaseConfig,
                 sql_logger: SqlLogger,
                 email_provider: EmailProvider,
                 application_config: ApplicationConfig,
                 config_service: ConfigService,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_rpc_client_config = process_rpc_client_config
        self.dispatcher = dispatcher
        self.config_service = config_service
        self.application_config = application_config
        self.email_provider = email_provider
        self.sql_logger = sql_logger
        self.database_config = database_config

    def connect_rpc(self):
        conn = connect(self.process_rpc_client_config.host, self.process_rpc_client_config.port)
        conn._config['timeout'] = 240
        conn.ASYNC_REQUEST_TIMEOUT = 240
        conn._config['sync_request_timeout'] = 240  # Set timeout to 240 seconds
        return conn

    @transactionhandler
    def handle(self, command: StartProcessCommand):
        """
        :param command: command
        :return:
        """

        conn = self.connect_rpc()
        conn.root.job_start(command.DataOperationId, command.JobId, command.DataOperationJobExecutionId)

