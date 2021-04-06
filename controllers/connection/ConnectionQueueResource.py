import json

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.services.ConnectionService import ConnectionService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.json.JsonConvert import JsonConvert
from models.viewmodels.connection.CreateConnectionQueueModel import CreateConnectionQueueModel


@ConnectionModels.ns.route("/ConnectionQueue")
class ConnectionQueueResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.expect(ConnectionModels.create_connection_queue_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Create New Queue Connection
        """
        data: CreateConnectionQueueModel = JsonConvert.FromJSON(json.dumps(IocManager.api.payload))
        creation_result = self.connection_service.create_connection_queue(data)
        result = ConnectionModels.get_connection_result_model(creation_result)
        return CommonModels.get_response(result=result)
