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
                 DataIntegration=None,
                 Database=None,
                 File=None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: int = Id
        self.SourceOrTarget: int = SourceOrTarget
        self.DataIntegration = DataIntegration
        self.Database = Database
        self.File = File
        self.Connection = Connection


class DataIntegrationConnectionDatabaseModel:

    def __init__(self,
                 Id: int = None,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query


class DataIntegrationConnectionFileModel:

    def __init__(self,
                 Id: int = None,
                 FileName: str = None,
                 *args, **kwargs):
        self.Id: int = Id
        self.FileName: str = FileName


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

    data_integration_connection_database_model = IocManager.api.model('DataIntegrationConnetionDatabaseModel', {
        'Schema': fields.String(description='Schema', required=False),
        'TableName': fields.String(description='TableName', required=False),
        'Query': fields.String(description='Query', required=False),
    })
    data_integration_connection_file_model = IocManager.api.model('DataIntegrationConnetionFileModel', {
        'FileName': fields.String(description='FileName', required=False)
    })
    data_integration_connection_model = IocManager.api.model('DataIntegrationConnetionModel', {
        'ConnectionName': fields.String(description='ConnectionName', required=False),
        'Database': fields.Nested(data_integration_connection_database_model, description='Database connection'),
        'File': fields.Nested(data_integration_connection_file_model, description='File connection'),
        'Columns': fields.String(description='Columns'),
    })

    data_integration_model = IocManager.api.model('DataIntegrationModel', {
        'Code': fields.String(description='Operation code value', required=True),
        'SourceConnections': fields.Nested(data_integration_connection_model, description='Source Connections',
                                           required=False),
        'TargetConnections': fields.Nested(data_integration_connection_model,
                                           description='Target Connections',
                                           required=True),
        'IsTargetTruncate': fields.Boolean(description='IsTargetTruncate', required=True),
        'IsDelta': fields.Boolean(description='IsDelta'),
        'Comments': fields.String(description='Comments'),
    })

    @staticmethod
    def get_data_integration_model(data_integration: DataIntegration) -> DataIntegrationModel:
        source_list = [x for x in data_integration.Connections if x.SourceOrTarget == 0]
        source = None
        if source_list is not None and len(source_list) > 0:
            source_connection = source_list[0]
            entity_source = DataIntegrationConnectionModel(
                Id=source_connection.Id,
                SourceOrTarget=source_connection.SourceOrTarget
            )
            source = json.loads(json.dumps(entity_source.__dict__, default=CommonModels.date_converter))

            if source_connection.Database is not None:
                entity_source_database = DataIntegrationConnectionDatabaseModel(
                    Id=source_connection.Id,
                    Schema=source_connection.Database.Schema,
                    TableName=source_connection.Database.TableName,
                    Query=source_connection.Database.Query,
                )
                source_database = json.loads(json.dumps(entity_source_database.__dict__, default=CommonModels.date_converter))
                source['Database'] = source_database
            if source_connection.File is not None:
                entity_source_file = DataIntegrationConnectionFileModel(
                    Id=source_connection.Id,
                    FileName=source_connection.File.FileName
                )
                source_file = json.loads(json.dumps(entity_source_file.__dict__, default=CommonModels.date_converter))
                source['File'] = source_file

            source['Connection'] = ConnectionModels.get_connection_result_model(source_connection.Connection)

        target_connection = [x for x in data_integration.Connections if x.SourceOrTarget == 1][0]
        entity_target = DataIntegrationConnectionModel(
            Id=target_connection.Id,
            SourceOrTarget=target_connection.SourceOrTarget
        )
        target = json.loads(json.dumps(entity_target.__dict__, default=CommonModels.date_converter))

        if target_connection.Database is not None:
            entity_target_database = DataIntegrationConnectionDatabaseModel(
                Id=target_connection.Id,
                Schema=target_connection.Database.Schema,
                TableName=target_connection.Database.TableName,
                Query=target_connection.Database.Query,
            )
            target_database = json.loads(json.dumps(entity_target_database.__dict__, default=CommonModels.date_converter))
            target['Database'] = target_database
        if target_connection.File is not None:
            entity_target_file = DataIntegrationConnectionFileModel(
                Id=target_connection.Id,
                FileName=target_connection.File.FileName
            )
            target_file = json.loads(json.dumps(entity_target_file.__dict__, default=CommonModels.date_converter))
            target['File'] = target_file
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
        if source is not None:
            result_model['SourceConnection'] = source
        result_model['TargetConnection'] = target
        result_model['Columns'] = columns
        return result_model

    @staticmethod
    def get_data_integration_models(data_integrations: List[DataIntegration]) -> List[DataIntegrationModel]:

        entities = []
        for data_integration in data_integrations:
            if data_integration.IsDeleted == 0:
                entity = DataIntegrationModels.get_data_integration_model(data_integration)
                entities.append(entity)
        return entities
