import json
from datetime import datetime, timedelta
from typing import List

from flask_restplus import fields
from flask_restplus.fields import Raw, MarshallingError

from controllers.models.CommonModels import EntityModel, CommonModels
from controllers.models.JobSchedulerModels import JobSchedulerModels
from controllers.models.PythonDataIntegrationModels import PythonDataIntegrationModels
from infrastructor.IocManager import IocManager
from models.dao.integration.PythonDataIntegrationJob import PythonDataIntegrationJob
from models.dao.integration.PythonDataIntegrationLog import PythonDataIntegrationLog
from models.dao.operation import DataOperation


class DataOperationIntegrationModel(EntityModel):

    def __init__(self,
                 Order: int = None,
                 Integration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Order: int = Order
        self.Integration = Integration


class DataOperationModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.Name: str = Name
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount


class PythonDataIntegrationJobModel(EntityModel):
    def __init__(self,
                 Id: int = None,
                 Code: str = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 PythonDataIntegrationId: int = None,
                 ApSchedulerJobId: int = None,
                 PythonDataIntegration=None,
                 ApSchedulerJob=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.Code: str = Code
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.PythonDataIntegrationId: int = PythonDataIntegrationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.PythonDataIntegration = PythonDataIntegration
        self.ApSchedulerJob = ApSchedulerJob
        self.IsDeleted = IsDeleted


class PythonDataIntegrationLogModel():

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
    })

    create_data_operation_model = IocManager.api.model('CreateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
        'Limit': fields.Integer(description='Operation code value', required=False, example=10000),
        'ProcessCount': fields.Integer(description='Operation code value', required=True, example=1)
    })

    update_data_operation_model = IocManager.api.model('UpdateDataOperation', {
        'Name': fields.String(description='Data Operation Name', required=True),
        'Integrations': fields.List(fields.Nested(operation_integration), description='Integration code list',
                                    required=True),
        'Limit': fields.Integer(description='Paging Limit Information', required=False, example=10000),
        'ProcessCount': fields.Integer(description='Configure your parallel process', required=False, example=1),
    })

    delete_data_operation_model = IocManager.api.model('DeleteDataOperationModel', {
        'Id': fields.Integer(description='Connection Database Id', required=True),
    })

    start_operation_model = IocManager.api.model('StartOperation', {
        'Code': fields.String(description='Operation code value', required=True),
        'RunDate': fields.DateTime(
            description="Job run date.", required=True,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'))
    })
    start_operation_with_cron_model = IocManager.api.model('StartOperationWithCron', {
        'Code': fields.String(description='Operation code value', required=True),
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
            Limit=data_operation.Limit,
            ProcessCount=data_operation.ProcessCount,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        integrations = []
        for data_operation_integration in data_operation.Integrations:
            entity_model = DataOperationIntegrationModel(
                Id=data_operation_integration.Id,
                Order=data_operation_integration.Order,
            )
            data_operation_integration_result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
            integration = PythonDataIntegrationModels.get_pdi_model(data_operation_integration.PythonDataIntegration)
            data_operation_integration_result_model['Integration']=integration
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
    def get_pdi_job_model(python_data_integration_job: PythonDataIntegrationJob) -> PythonDataIntegrationJobModel:
        entity_model = PythonDataIntegrationJobModel(
            Id=python_data_integration_job.Id,
            Cron=python_data_integration_job.Cron,
            StartDate=python_data_integration_job.StartDate,
            EndDate=python_data_integration_job.EndDate,
            PythonDataIntegrationId=python_data_integration_job.PythonDataIntegrationId,
            ApSchedulerJobId=python_data_integration_job.ApSchedulerJobId,
            IsDeleted=python_data_integration_job.IsDeleted,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        result_model['PythonDataIntegration'] = PythonDataIntegrationModels.get_pdi_model(
            python_data_integration_job.PythonDataIntegration),
        result_model['ApSchedulerJob'] = JobSchedulerModels.get_ap_scheduler_job_model(
            python_data_integration_job.ApSchedulerJob)
        return result_model

    @staticmethod
    def get_pdi_job_models(python_data_integration_jobs: List[PythonDataIntegrationJob]) -> List[
        PythonDataIntegrationJob]:
        entities = []
        for python_data_integration_job in python_data_integration_jobs:
            entity = DataOperationModels.get_pdi_job_model(python_data_integration_job)
            entities.append(entity)
        return entities

    @staticmethod
    def get_pdi_logs_model(python_data_integration_logs: List[PythonDataIntegrationLog]) -> List[
        PythonDataIntegrationLogModel]:

        entities = []
        for python_data_integration_log in python_data_integration_logs:
            result = PythonDataIntegrationLogModel(
                Id=python_data_integration_log.Id,
                JobId=python_data_integration_log.JobId,
                Type='Info' if python_data_integration_log.TypeId == 2 else 'Error',
                Content=python_data_integration_log.Content,
                LogDatetime=python_data_integration_log.LogDatetime,
            )
            entity = json.loads(json.dumps(result.__dict__, default=CommonModels.date_converter))
            entities.append(entity)
        return entities
