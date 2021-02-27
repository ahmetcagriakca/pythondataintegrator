from models.dao.operation import DataOperationJob
from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.operation.models.JobSchedulerModels import JobSchedulerModels
from domain.operation.services.DataOperationService import DataOperationService
from domain.job.services.JobOperationService import JobOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


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
        Schedule Data Operation cron job
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        cron = data.get('Cron')  #
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        start_operation_result = self.job_operation_service.add_pdi_job_with_cron(operation_name=operation_name,
                                                                                  cron=cron,
                                                                                  start_date=start_date,
                                                                                  end_date=end_date)
        result = JobSchedulerModels.get_data_operation_job_model(start_operation_result)
        return CommonModels.get_response(result=result)

    @JobSchedulerModels.ns.expect(JobSchedulerModels.start_operation_with_cron_model,
                                  validate=True)
    @JobSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def put(self):
        """
        Update existing Data Operation cron job
        """
        data = IocManager.api.payload
        operation_name = data.get('OperationName')  #
        cron = data.get('Cron')  #
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        start_operation_result = self.job_operation_service.modify_job(operation_name=operation_name, cron=cron, start_date=start_date,
                                                                       end_date=end_date)
        if isinstance(start_operation_result, DataOperationJob):
            result = JobSchedulerModels.get_data_operation_job_model(start_operation_result)
            return CommonModels.get_response(result=result)
        else:
            message = start_operation_result
            return CommonModels.get_error_response(message=message)
