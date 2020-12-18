import json

from injector import inject
from controllers.models.CommonModels import CommonModels
from controllers.models.ConnectionModels import ConnectionModels
from domain.pdi.services.ConnectionService import ConnectionService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.CreateConnectionDatabaseModel import CreateConnectionDatabaseModel
from models.viewmodels.UpdateConnectionDatabaseModel import UpdateConnectionDatabaseModel


@ConnectionModels.ns.route("/GetConnectionTypes")
class GetConnectionTypesResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get Connection Types
        """
        connection_types = self.connection_service.get_connection_types()
        result = ConnectionModels.get_connection_type_models(connection_types)
        return CommonModels.get_response(result=result)


@ConnectionModels.ns.route("/GetConnectorTypes")
class GetConnectorTypesResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get Connector Types
        """
        connector_types = self.connection_service.get_connector_types()
        result = ConnectionModels.get_connector_type_models(connector_types)
        return CommonModels.get_response(result=result)

@ConnectionModels.ns.route("/Conection")
class GetConnectionResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service


    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Connections
        """
        connections = self.connection_service.get_connections()
        result = ConnectionModels.get_connection_result_models(connections)
        return CommonModels.get_response(result=result)

@ConnectionModels.ns.route("/ConectionDatabase")
class GetConectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service


    @ConnectionModels.ns.expect(ConnectionModels.create_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create New Database Connection
        """
        data: CreateConnectionDatabaseModel = json.loads(json.dumps(IocManager.api.payload),
                                                         object_hook=lambda d: CreateConnectionDatabaseModel(**d))
        creation_result = self.connection_service.create_connection_database(data)
        result = ConnectionModels.get_connection_result_model(creation_result)
        return CommonModels.get_response(result=result)

    @ConnectionModels.ns.expect(ConnectionModels.update_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def put(self):
        """
        Update Existing Database Connection
        """

        data: CreateConnectionDatabaseModel = json.loads(json.dumps(IocManager.api.payload),
                                                         object_hook=lambda d: UpdateConnectionDatabaseModel(**d))
        creation_result = self.connection_service.update_connection_database(data)
        result = ConnectionModels.get_connection_result_model(creation_result)
        return CommonModels.get_response(result=result)

    @ConnectionModels.ns.expect(ConnectionModels.delete_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Database Connection
        """
        data = IocManager.api.payload
        id = data.get('Id')  #
        deletion_result = self.connection_service.delete_connection_database(id)
        return CommonModels.get_response(message="Connection Removed Successfully")
