import json
from typing import List

from flask_restplus import fields

from controllers.common.models.CommonModels import EntityModel, CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from infrastructor.IocManager import IocManager
from models.dao.integration.DataIntegration import DataIntegration


class DataIntegrationModel(EntityModel):

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


class DataIntegrationConnectionModel:

    def __init__(self,
                 Id: int = None,
                 SourceOrTarget: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 DataIntegration=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.SourceOrTarget: int = SourceOrTarget
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.DataIntegration = DataIntegration
        self.Connection = Connection


class DataIntegrationColumnModel:

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


class DataIntegrationModels:
    ns = IocManager.api.namespace('DataIntegration', description='Data Integration endpoints',
                                  path='/api/DataIntegration')
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
    def get_pdi_model(data_integration: DataIntegration) -> DataIntegrationModel:
        source_connection = data_integration.Connections[0]
        entity_source = DataIntegrationConnectionModel(
            Id=source_connection.Id,
            SourceOrTarget=source_connection.SourceOrTarget,
            Schema=source_connection.Schema,
            TableName=source_connection.TableName)
        source = json.loads(json.dumps(entity_source.__dict__, default=CommonModels.date_converter))
        source['Connection'] = ConnectionModels.get_connection_result_model(source_connection.Connection)

        target_connection = data_integration.Connections[1]
        entity_target = DataIntegrationConnectionModel(
            Id=target_connection.Id,
            SourceOrTarget=target_connection.SourceOrTarget,
            Schema=target_connection.Schema,
            TableName=target_connection.TableName)
        target = json.loads(json.dumps(entity_target.__dict__, default=CommonModels.date_converter))
        target['Connection'] = ConnectionModels.get_connection_result_model(target_connection.Connection)
        columns = []
        for col in data_integration.Columns:
            entity_column = DataIntegrationColumnModel(
                Id=col.Id,
                ResourceType=col.ResourceType,
                SourceColumnName=col.SourceColumnName,
                TargetColumnName=col.TargetColumnName,
            )
            column = json.loads(json.dumps(entity_column.__dict__, default=CommonModels.date_converter))
            columns.append(column)
        entity_model = DataIntegrationModel(
            Id=data_integration.Id,
            Code=data_integration.Code,
            IsTargetTruncate=data_integration.IsTargetTruncate,
            IsDelta=data_integration.IsDelta,
            CreationDate=data_integration.CreationDate,
            Comments=data_integration.Comments,
            IsDeleted=data_integration.IsDeleted
        )

        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))

        result_model['SourceConnection'] = source
        result_model['TargetConnection'] = target
        result_model['Columns'] = columns
        return result_model

    @staticmethod
    def get_pdi_models(data_integrations: List[DataIntegration]) -> List[DataIntegrationModel]:

        entities = []
        for data_integration in data_integrations:
            entity = DataIntegrationModels.get_pdi_model(data_integration)
            entities.append(entity)
        return entities
