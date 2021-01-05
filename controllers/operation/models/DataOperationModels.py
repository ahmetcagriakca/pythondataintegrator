import json
from datetime import datetime, timedelta
from typing import List

from flask_restplus import fields
from flask_restplus.fields import Raw

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.job.models.JobModels import JobModels
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
        'Limit': fields.Integer(description='Operation code value', required=False, example=10000),
        'ProcessCount': fields.Integer(description='Operation code value', required=True, example=1),
        'Integration': fields.Nested(DataIntegrationModels.create_data_integration_model,
                                     description='Integration information', required=True)
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
