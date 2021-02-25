from typing import List

from injector import inject

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.operation import Definition
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob
from models.viewmodels.integration.UpdateDataIntegrationModel import UpdateDataIntegrationModel


class DataIntegrationExecutionJobService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_execution_job_repository: Repository[DataIntegrationExecutionJob] = Repository[
            DataIntegrationExecutionJob](database_session_manager)

    #######################################################################################

    def insert(self,
               data_integration: DataIntegration,
               pre_executions: str,
               post_executions: str):
        if pre_executions is not None and pre_executions != "":
            self.insert_execution_job(pre_executions, 1, 0, data_integration)
        if post_executions is not None and post_executions != "":
            self.insert_execution_job(post_executions, 0, 1, data_integration)

    def insert_execution_job(self, execution_list, is_pre, is_post, DataIntegration):
        pre_execution_list = execution_list.split(",")
        for preExecution in pre_execution_list:
            data_integration_execution_job = DataIntegrationExecutionJob(ExecutionProcedure=preExecution,
                                                                         IsPre=is_pre,
                                                                         IsPost=is_post,
                                                                         DataIntegration=DataIntegration)
            self.data_integration_execution_job_repository.insert(data_integration_execution_job)

    def update_execution_job(self, execution_jobs, is_pre, is_post, data_integration: DataIntegration):
        execution_job_list = execution_jobs.split(",")
        for execution_job in execution_job_list:
            data_integration_execution_job = self.data_integration_execution_job_repository.first(
                IsDeleted=0,
                IsPre=is_pre,
                IsPost=is_post,
                ExecutionProcedure=execution_job,
                DataIntegration=data_integration)
            if data_integration_execution_job is None:
                data_integration_execution_job = DataIntegrationExecutionJob(ExecutionProcedure=execution_job,
                                                                             IsPre=is_pre,
                                                                             IsPost=is_post,
                                                                             DataIntegration=data_integration)
                self.data_integration_execution_job_repository.insert(data_integration_execution_job)

        data_integration_execution_jobs = self.data_integration_execution_job_repository.filter_by(
            IsDeleted=0,
            DataIntegration=data_integration,
            IsPre=is_pre,
            IsPost=is_post)
        for data_integration_execution_job in data_integration_execution_jobs:
            check_execution = [execution for execution in execution_job_list if
                               execution == data_integration_execution_job.ExecutionProcedure]
            if not (check_execution is not None and len(check_execution) > 0 and check_execution[0] is not None):
                self.data_integration_execution_job_repository.delete(data_integration_execution_job)

    def delete_execution_job(self, is_pre, is_post, data_integration):
        data_integration_execution_jobs = self.data_integration_execution_job_repository.filter_by(
            IsDeleted=0,
            DataIntegration=data_integration,
            IsPre=is_pre,
            IsPost=is_post)
        for data_integration_execution_job in data_integration_execution_jobs:
            self.data_integration_execution_job_repository.delete(data_integration_execution_job)

    def update(self,
               data_integration: DataIntegration,
               pre_executions: str,
               post_executions: str):
        if pre_executions is not None and pre_executions != "":
            self.update_execution_job(pre_executions, True, False, data_integration)
        else:
            self.delete_execution_job(True, False, data_integration)
        if post_executions is not None and post_executions != "":
            self.update_execution_job(post_executions, False, True, data_integration)
        else:
            self.delete_execution_job(False, True, data_integration)
        return data_integration

    def delete(self, id: int):
        self.data_integration_execution_job_repository.delete_by_id(id)
