import json
from datetime import datetime, timedelta
from typing import List

from flask_restplus import fields
from flask_restplus.fields import Raw

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.job.models.JobSchedulerModels import JobSchedulerModels
from controllers.integration.models.DataIntegrationModels import DataIntegrationModels
from infrastructor.IocManager import IocManager
from models.dao.common.Log import Log
from models.dao.operation import DataOperation, DataOperationJob


class DataOperationIntegrationModel(EntityModel):

    def __init__(self,
                 Order: int = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 Integration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.Integration = Integration


class DataOperationModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.Name: str = Name


class DataOperationJobModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 Code: str = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 DataIntegration=None,
                 ApSchedulerJob=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.Code: str = Code
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.DataOperationId: int = DataOperationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.DataIntegration = DataIntegration
        self.ApSchedulerJob = ApSchedulerJob
        self.IsDeleted = IsDeleted


class DataIntegrationLogModel():

    def __init__(self,
                 Id: int = None,
                 Type: str = None,
                 Content: str = None,
                 LogDatetime: datetime = None,
                 JobId: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Type = Type
        self.Content = Content
        self.LogDatetime = LogDatetime
        self.JobId = JobId


class OperationIntegration(Raw):
    def __init__(self,
                 Code: str = None,
                 Order: int = None,
                 *args, **kwargs):
        self.Code = Code
        self.Order = Order


class DataOperationModels:
    ns = IocManager.api.namespace('DataOperation', description='Data Operation endpoints',
                                  path='/api/DataOperation')

    operation_integration = IocManager.api.model('test', {
        'Code': fields.String(description='Integration code', required=True),
        'Order': fields.Integer(description='Integration order', required=True, example=1),
        'Limit': fields.Integer(description='Operation code value', required=False, example=10000),
        'ProcessCount': fields.Integer(description='Operation code value', required=True, example=1)
    })

    create_data_operation_model = IocManager.api.model('CreateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
    })

    update_data_operation_model = IocManager.api.model('UpdateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
    })

    delete_data_operation_model = IocManager.api.model('DeleteDataOperationModel', {
        'Id': fields.Integer(description='Connection Database Id', required=True),
    })

    start_operation_model = IocManager.api.model('Schedule', {
        'OperationName': fields.String(description='Operation name', required=True),
        'RunDate': fields.DateTime(
            description="Job run date.", required=True,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'))
    })
    start_operation_with_cron_model = IocManager.api.model('ScheduleDataOperation', {
        'OperationName': fields.String(description='Operation name', required=True),
        'Cron': fields.String(description="Job cron value. ", required=True, example='*/1 * * * *'),
        'StartDate': fields.DateTime(
            description="Job start date. The start date for the job can be entered if necessary.", required=False,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')),
        'EndDate': fields.DateTime(
            description="Job End date. The end date for the job can be entered if necessary.", required=False,
            example=(datetime.now() + timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
    })

    @staticmethod
    def get_data_operation_result_model(data_operation: DataOperation) -> DataOperationModel:
        entity_model = DataOperationModel(
            Id=data_operation.Id,
            Name=data_operation.Name,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        integrations = []
        for data_operation_integration in data_operation.Integrations:
            entity_model = DataOperationIntegrationModel(
                Id=data_operation_integration.Id,
                Order=data_operation_integration.Order,
                Limit=data_operation_integration.Limit,
                ProcessCount=data_operation_integration.ProcessCount,
            )
            data_operation_integration_result_model = json.loads(
                json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
            integration = DataIntegrationModels.get_data_integration_model(data_operation_integration.DataIntegration)
            data_operation_integration_result_model['Integration'] = integration
            integrations.append(data_operation_integration_result_model)
        result_model['Integrations'] = integrations
        return result_model

    @staticmethod
    def get_data_operation_result_models(data_operations: List[DataOperation]) -> List[DataOperationModel]:
        entities = []
        for data_operation in data_operations:
            entity = DataOperationModels.get_data_operation_result_model(data_operation)
            entities.append(entity)
        return entities

    @staticmethod
    def get_data_operation_job_model(data_operation_job: DataOperationJob) -> DataOperationJobModel:
        entity_model = DataOperationJobModel(
            Id=data_operation_job.Id,
            Cron=data_operation_job.Cron,
            StartDate=data_operation_job.StartDate,
            EndDate=data_operation_job.EndDate,
            DataOperationId=data_operation_job.DataOperationId,
            ApSchedulerJobId=data_operation_job.ApSchedulerJobId,
            IsDeleted=data_operation_job.IsDeleted,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['DataOperation'] = DataOperationModels.get_data_operation_result_model(
            data_operation_job.DataOperation),
        result_model['ApSchedulerJob'] = JobSchedulerModels.get_ap_scheduler_job_model(
            data_operation_job.ApSchedulerJob)
        return result_model

    @staticmethod
    def get_data_operation_job_models(data_operation_jobs: List[DataOperationJob]) -> List[
        DataOperationJobModel]:
        entities = []
        for data_operation_job in data_operation_jobs:
            entity = DataOperationModels.get_data_operation_job_model(data_operation_jobs)
            entities.append(entity)
        return entities

    @staticmethod
    def get_pdi_logs_model(logs: List[Log]) -> List[
        DataIntegrationLogModel]:

        entities = []
        for log in logs:
            result = DataIntegrationLogModel(
                Id=log.Id,
                JobId=log.JobId,
                Type='Info' if log.TypeId == 2 else 'Error',
                Content=log.Content,
                LogDatetime=log.LogDatetime,
            )
            entity = json.loads(json.dumps(result.__dict__, default=CommonModels.date_converter))
            entities.append(entity)
        return entities
