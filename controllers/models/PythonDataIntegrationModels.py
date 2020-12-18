import json
from typing import List

from flask_restplus import fields

from controllers.models.CommonModels import EntityModel, CommonModels
from controllers.models.ConnectionModels import ConnectionModels
from infrastructor.IocManager import IocManager
from models.dao.integration.PythonDataIntegration import PythonDataIntegration


class PythonDataIntegrationModel(EntityModel):

    def __init__(self,
                 Id=None,
                 Code=None,
                 IsTargetTruncate=None,
                 IsDelta=None,
                 CreationDate=None,
                 Comments=None,
                 IsDeleted=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.Code = Code
        self.IsTargetTruncate = IsTargetTruncate
        self.IsDelta = IsDelta
        self.CreationDate = CreationDate
        self.Comments = Comments
        self.IsDeleted = IsDeleted


class PythonDataIntegrationConnectionModel:

    def __init__(self,
                 Id: int = None,
                 SourceOrTarget: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 PythonDataIntegration=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.SourceOrTarget: int = SourceOrTarget
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.PythonDataIntegration = PythonDataIntegration
        self.Connection = Connection


class PythonDataIntegrationColumnModel:

    def __init__(self,
                 Id=None,
                 ResourceType=None,
                 SourceColumnName=None,
                 TargetColumnName=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id = Id
        self.ResourceType = ResourceType
        self.SourceColumnName = SourceColumnName
        self.TargetColumnName = TargetColumnName



class PythonDataIntegrationModels:

    ns = IocManager.api.namespace('PythonDataIntegration', description='Python Data Integration endpoints',
                                  path='/api/PythonDataIntegration')
    create_integration_data_model = IocManager.api.model('CreateIntegrationDataModel', {
        'Code': fields.String(description='Operation code value', required=True),
        'SourceConnectionId': fields.Integer(description='SourceConnectionId'),
        'SourceSchema': fields.String(description='SourceSchema'),
        'SourceTableName': fields.String(description='SourceTableName'),
        'TargetConnectionId': fields.Integer(description='TargetConnectionId'),
        'TargetSchema': fields.String(description='TargetSchema'),
        'TargetTableName': fields.String(description='TargetTableName'),
        'IsTargetTruncate': fields.Boolean(description='IsTargetTruncate'),
        'IsDelta': fields.Boolean(description='IsDelta'),
        'Comments': fields.String(description='Comments'),
        'SourceColumns': fields.String(description='SourceColumns'),
        'TargetColumns': fields.String(description='TargetColumns'),
        'PreExecutions': fields.String(description='PreExecutions'),
        'PostExecutions': fields.String(description='PostExecutions'),
    })

    update_integration_data_model = IocManager.api.model('UpdateIntegrationDataModel', {
        'Code': fields.String(description='Operation code value', required=True),
        'SourceConnectionId': fields.Integer(description='SourceConnectionId'),
        'SourceSchema': fields.String(description='SourceSchema'),
        'SourceTableName': fields.String(description='SourceTableName'),
        'TargetConnectionId': fields.Integer(description='TargetConnectionId'),
        'TargetSchema': fields.String(description='TargetSchema'),
        'TargetTableName': fields.String(description='TargetTableName'),
        'IsTargetTruncate': fields.Boolean(description='IsTargetTruncate'),
        'IsDelta': fields.Boolean(description='IsDelta'),
        'Comments': fields.String(description='Comments'),
        'SourceColumns': fields.String(description='SourceColumns'),
        'TargetColumns': fields.String(description='TargetColumns'),
        'PreExecutions': fields.String(description='PreExecutions'),
        'PostExecutions': fields.String(description='PostExecutions'),
    })

    delete_integration_data_model = IocManager.api.model('DeleteIntegrationDataModel', {
        'Code': fields.String(description='Operation code value', required=True),
    })

    @staticmethod
    def get_pdi_model(python_data_integration: PythonDataIntegration) -> PythonDataIntegrationModel:
        source_connection = python_data_integration.Connections[0]
        entity_source = PythonDataIntegrationConnectionModel(
            Id=source_connection.Id,
            SourceOrTarget=source_connection.SourceOrTarget,
            Schema=source_connection.Schema,
            TableName=source_connection.TableName)
        source = json.loads(json.dumps(entity_source.__dict__, default=CommonModels.date_converter))
        source['Connection'] = ConnectionModels.get_connection_result_model(source_connection.Connection)

        target_connection = python_data_integration.Connections[1]
        entity_target = PythonDataIntegrationConnectionModel(
            Id=target_connection.Id,
            SourceOrTarget=target_connection.SourceOrTarget,
            Schema=target_connection.Schema,
            TableName=target_connection.TableName)
        target = json.loads(json.dumps(entity_target.__dict__, default=CommonModels.date_converter))
        target['Connection'] = ConnectionModels.get_connection_result_model(target_connection.Connection)
        columns = []
        for col in python_data_integration.Columns:
            entity_column = PythonDataIntegrationColumnModel(
                Id=col.Id,
                ResourceType=col.ResourceType,
                SourceColumnName=col.SourceColumnName,
                TargetColumnName=col.TargetColumnName,
            )
            column = json.loads(json.dumps(entity_column.__dict__, default=CommonModels.date_converter))
            columns.append(column)
        entity_model = PythonDataIntegrationModel(
            Id=python_data_integration.Id,
            Code=python_data_integration.Code,
            IsTargetTruncate=python_data_integration.IsTargetTruncate,
            IsDelta=python_data_integration.IsDelta,
            CreationDate=python_data_integration.CreationDate,
            Comments=python_data_integration.Comments,
            IsDeleted=python_data_integration.IsDeleted
        )

        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))

        result_model['SourceConnection'] = source
        result_model['TargetConnection'] = target
        result_model['Columns'] = columns
        return result_model

    @staticmethod
    def get_pdi_models(python_data_integrations: List[PythonDataIntegration]) -> List[PythonDataIntegrationModel]:

        entities = []
        for python_data_integration in python_data_integrations:
            entity = PythonDataIntegrationModels.get_pdi_model(python_data_integration)
            entities.append(entity)
        return entities

