from injector import inject
from pdip.cqrs import Dispatcher
from pdip.dependency import IScoped
from pdip.integrator.base import IntegratorEventManager
from pdip.integrator.operation.domain import OperationBase, OperationIntegrationBase
from pdip.logging.loggers.sql import SqlLogger

from process.application.Events.ExecuteOperationFinish.ExecuteOperationFinishCommand import \
    ExecuteOperationFinishCommand
from process.application.Events.ExecuteOperationFinish.ExecuteOperationFinishRequest import \
    ExecuteOperationFinishRequest
from process.application.Events.ExecuteOperationInitialize.ExecuteOperationInitializeCommand import \
    ExecuteOperationInitializeCommand
from process.application.Events.ExecuteOperationInitialize.ExecuteOperationInitializeRequest import \
    ExecuteOperationInitializeRequest
from process.application.Events.ExecuteOperationIntegrationFinish.ExecuteOperationIntegrationFinishCommand import \
    ExecuteOperationIntegrationFinishCommand
from process.application.Events.ExecuteOperationIntegrationFinish.ExecuteOperationIntegrationFinishRequest import \
    ExecuteOperationIntegrationFinishRequest
from process.application.Events.ExecuteOperationIntegrationInitialize.ExecuteOperationIntegrationInitializeCommand import \
    ExecuteOperationIntegrationInitializeCommand
from process.application.Events.ExecuteOperationIntegrationInitialize.ExecuteOperationIntegrationInitializeRequest import \
    ExecuteOperationIntegrationInitializeRequest
from process.application.Events.ExecuteOperationIntegrationSource.ExecuteOperationIntegrationSourceCommand import \
    ExecuteOperationIntegrationSourceCommand
from process.application.Events.ExecuteOperationIntegrationSource.ExecuteOperationIntegrationSourceRequest import \
    ExecuteOperationIntegrationSourceRequest
from process.application.Events.ExecuteOperationIntegrationStart.ExecuteOperationIntegrationStartCommand import \
    ExecuteOperationIntegrationStartCommand
from process.application.Events.ExecuteOperationIntegrationStart.ExecuteOperationIntegrationStartRequest import \
    ExecuteOperationIntegrationStartRequest
from process.application.Events.ExecuteOperationIntegrationTarget.ExecuteOperationIntegrationTargetCommand import \
    ExecuteOperationIntegrationTargetCommand
from process.application.Events.ExecuteOperationIntegrationTarget.ExecuteOperationIntegrationTargetRequest import \
    ExecuteOperationIntegrationTargetRequest
from process.application.Events.ExecuteOperationIntegrationTargetTruncate.ExecuteOperationIntegrationTargetTruncateCommand import \
    ExecuteOperationIntegrationTargetTruncateCommand
from process.application.Events.ExecuteOperationIntegrationTargetTruncate.ExecuteOperationIntegrationTargetTruncateRequest import \
    ExecuteOperationIntegrationTargetTruncateRequest
from process.application.Events.ExecuteOperationStart.ExecuteOperationStartCommand import \
    ExecuteOperationStartCommand
from process.application.Events.ExecuteOperationStart.ExecuteOperationStartRequest import \
    ExecuteOperationStartRequest
from process.application.Events.LogIntegrator.LogIntegratorCommand import LogIntegratorCommand
from process.application.Events.LogIntegrator.LogIntegratorRequest import LogIntegratorRequest


class ProcessIntegratorEventManager(IScoped, IntegratorEventManager):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.logger = logger

    def log(self, data: any, message: str, exception=None):
        req = LogIntegratorRequest(Data=data, Message=message, Exception=exception)
        command = LogIntegratorCommand(request=req)
        self.dispatcher.dispatch(command)

    def initialize(self, data: OperationBase):
        req = ExecuteOperationInitializeRequest(Operation=data)
        command = ExecuteOperationInitializeCommand(request=req)
        self.dispatcher.dispatch(command)

    def start(self, data: OperationBase):
        req = ExecuteOperationStartRequest(Operation=data)
        command = ExecuteOperationStartCommand(request=req)
        self.dispatcher.dispatch(command)

    def finish(self, data: OperationBase, exception=None):
        req = ExecuteOperationFinishRequest(Operation=data, Exception=exception)
        command = ExecuteOperationFinishCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_initialize(self, data: OperationIntegrationBase, message):
        req = ExecuteOperationIntegrationInitializeRequest(OperationIntegration=data, Message=message)
        command = ExecuteOperationIntegrationInitializeCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_start(self, data: OperationIntegrationBase, message):
        req = ExecuteOperationIntegrationStartRequest(OperationIntegration=data, Message=message)
        command = ExecuteOperationIntegrationStartCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_finish(self, data: OperationIntegrationBase, data_count, message, exception=None):
        req = ExecuteOperationIntegrationFinishRequest(OperationIntegration=data, Message=message, Exception=exception)
        command = ExecuteOperationIntegrationFinishCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_target_truncate(self, data: OperationIntegrationBase, row_count):
        req = ExecuteOperationIntegrationTargetTruncateRequest(OperationIntegration=data, RowCount=row_count)
        command = ExecuteOperationIntegrationTargetTruncateCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_execute_source(self, data: OperationIntegrationBase, row_count):
        req = ExecuteOperationIntegrationSourceRequest(OperationIntegration=data, RowCount=row_count)
        command = ExecuteOperationIntegrationSourceCommand(request=req)
        self.dispatcher.dispatch(command)

    def integration_execute_target(self, data: OperationIntegrationBase, row_count):
        req = ExecuteOperationIntegrationTargetRequest(OperationIntegration=data, RowCount=row_count)
        command = ExecuteOperationIntegrationTargetCommand(request=req)
        self.dispatcher.dispatch(command)
