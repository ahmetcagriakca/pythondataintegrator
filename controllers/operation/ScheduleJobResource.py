from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.JobSchedulerModels import JobSchedulerModels
from domain.operation.services.DataOperationService import DataOperationService
from domain.job.services.JobOperationService import JobOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


@JobSchedulerModels.ns.route("/ScheduleJob")
class ScheduleJobResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service
        self.data_operation_service = data_operation_service

    @JobSchedulerModels.ns.expect(JobSchedulerModels.start_operation_model, validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Schedule Data Operation
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        run_date = data.get('RunDate')  #
        start_operation_result = self.job_operation_service.insert_job_with_date(operation_name=operation_name,
                                                                                 run_date=run_date)
        result = JobSchedulerModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)

    @JobSchedulerModels.ns.expect(JobSchedulerModels.delete_operation_job_model, validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Date Job
        """
        data = IocManager.api.payload
        data_operation_job_id = data.get('DataOperationJobId')  #
        deletion_result = self.job_operation_service.delete_scheduler_date_job(data_operation_job_id=data_operation_job_id)
        return CommonModels.get_response(message="Data Operation Job removed successfully")
