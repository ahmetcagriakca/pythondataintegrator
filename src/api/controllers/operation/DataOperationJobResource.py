import json

from flask import request

from domain.operation.GetDataOperationJobList.DataOperationJobListQuery import DataOperationJobListQuery
from domain.operation.GetDataOperationJobList.DataOperationJobListQueryHandler import DataOperationJobListQueryHandler
from domain.operation.GetDataOperationJobList.DataOperationJobListRequest import DataOperationJobListRequest
from infrastructor.json.JsonConvert import JsonConvert

from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from infrastructor.api.ResourceBase import ResourceBase


@DataOperationModels.ns.route("/Job")
class DataOperationJobResource(ResourceBase):
    @inject
    def __init__(self,
                 data_operation_job_list_query_handler: DataOperationJobListQueryHandler,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_job_list_query_handler = data_operation_job_list_query_handler

    @DataOperationModels.ns.expect(DataOperationModels.get_data_operation_jobs_parser, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        """
        Get All Data Operation Jobs
        """
        data = DataOperationModels.get_data_operation_jobs_parser.parse_args(request)
        req: DataOperationJobListRequest = JsonConvert.FromJSON(json.dumps(data))
        query = DataOperationJobListQuery(request=req)
        res = self.data_operation_job_list_query_handler.handle(query=query)
        result = json.loads(json.dumps(res.to_dict(), default=CommonModels.date_converter))
        return CommonModels.get_response(result=result)
