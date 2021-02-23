import json

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.services.ConnectionService import ConnectionService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.connection.CreateConnectionFileModel import CreateConnectionFileModel


@ConnectionModels.ns.route("/ConnectionFile")
class ConnectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.expect(ConnectionModels.create_connection_file_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create New Database Connection
        """
        data: CreateConnectionFileModel = json.loads(json.dumps(IocManager.api.payload),
                                                     object_hook=lambda d: CreateConnectionFileModel(**d))
        creation_result = self.connection_service.create_connection_file(data)
        result = ConnectionModels.get_connection_result_model(creation_result)
        return CommonModels.get_response(result=result)
