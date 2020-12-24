from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.DataOperationModels import DataOperationModels
from domain.operation.services.DataOperationService import DataOperationService
from domain.job.services.JobOperationService import JobOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


@DataOperationModels.ns.route("/ScheduleJob")
class ScheduleJobResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service
        self.data_operation_service = data_operation_service

    @DataOperationModels.ns.expect(DataOperationModels.start_operation_model, validate=True)
    @DataOperationModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Schedule Data Operation
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        run_date = data.get('RunDate')  #
        start_operation_result = self.job_operation_service.add_pdi_job_with_date(operation_name=operation_name, run_date=run_date)
        result = DataOperationModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)

