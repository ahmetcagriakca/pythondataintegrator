import json

from flask import request

from domain.operation.GetDataOperationList.DataOperationListQuery import DataOperationListQuery
from domain.operation.GetDataOperationList.DataOperationListQueryHandler import DataOperationListQueryHandler
from domain.operation.GetDataOperationList.DataOperationListRequest import DataOperationListRequest
from domain.operation.GetDataOperationList.DataOperationListResponse import DataOperationListResponse
from infrastructor.json.JsonConvert import JsonConvert

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from domain.operation.services.DataOperationService import DataOperationService
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from models.viewmodels.operation.CreateDataOperationModel import CreateDataOperationModel


@DataOperationModels.ns.route("")
class DataOperationResource(ResourceBase):
    @inject
    def __init__(self,
                 data_operation_service: DataOperationService,
                 data_operation_list_query_handler: DataOperationListQueryHandler,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_list_query_handler = data_operation_list_query_handler
        self.data_operation_service = data_operation_service

    @DataOperationModels.ns.expect(CommonModels.request_parser(DataOperationListRequest), validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.api_model(DataOperationListResponse))
    def get(self):
        """
        Get All Data Operations
        """
        req = CommonModels.get_request(DataOperationListRequest)
        query = DataOperationListQuery(request=req)
        res = self.connection_list_query_handler.handle(query=query)
        result = json.loads(json.dumps(res.to_dict(), default=CommonModels.date_converter))
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.create_data_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Data Operation definition
        """
        data: CreateDataOperationModel = JsonConvert.FromJSON(json.dumps(IocManager.api.payload))
        creation_result = self.data_operation_service.post_data_operation(
            data_operation_model=data,
            definition_json=JsonConvert.ToJSON(data))
        result = DataOperationModels.get_data_operation_result_model(creation_result)
        return CommonModels.get_response(result=result)

    @DataOperationModels.ns.expect(DataOperationModels.delete_data_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Data Operation
        """
        data = IocManager.api.payload
        id = data.get('Id')  #
        deletion_result = self.data_operation_service.delete_data_operation(id)
        return CommonModels.get_response(message="Data Operation removed successfully")
