from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.JobSchedulerModels import JobSchedulerModels
from domain.operation.services.DataOperationService import DataOperationService
from domain.job.services.JobOperationService import JobOperationService
from IocManager import IocManager
from infrastructure.api.ResourceBase import ResourceBase


@JobSchedulerModels.ns.route("/ScheduleJobWithCron")
class ScheduleJobWithCronResource(ResourceBase):
    @inject
    def __init__(self, data_operation_service: DataOperationService,
                 job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service
        self.data_operation_service = data_operation_service

    @JobSchedulerModels.ns.expect(JobSchedulerModels.start_operation_with_cron_model, validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Schedule Data Operation Cron Job
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        cron = data.get('Cron')  #
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        start_operation_result = self.job_operation_service.create_job_with_cron(operation_name=operation_name,
                                                                                 cron=cron,
                                                                                 start_date=start_date,
                                                                                 end_date=end_date)
        result = JobSchedulerModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)

    @JobSchedulerModels.ns.expect(JobSchedulerModels.delete_operation_cron_job_model, validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def delete(self):
        """
        Delete Existing Cron Job
        """
        data = IocManager.api.payload
        data_operation_name = data.get('DataOperationName')  #
        deletion_result = self.job_operation_service.delete_scheduler_cron_job(data_operation_name=data_operation_name)
        return CommonModels.get_response(message="Data Operation Job Cron removed successfully")
