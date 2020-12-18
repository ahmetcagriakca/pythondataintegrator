from datetime import datetime

from injector import inject

from controllers.models.CommonModels import CommonModels
from controllers.models.JobSchedulerModels import JobSchedulerModels
from controllers.models.TestParallelModels import TestParallelModels
from domain.pdi.services.JobOperationService import JobOperationService
from domain.pdi.services.TestParallelService import TestParallelService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


@TestParallelModels.ns.route('/StartParallel/<int:value>')
class TestParallelResource(ResourceBase):
    @inject
    def __init__(self, test_parallel_service: TestParallelService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_parallel_service = test_parallel_service

    @TestParallelModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, value):
        result = self.test_parallel_service.test_performance_parallel(value)
        return CommonModels.get_response(message=result)


@TestParallelModels.ns.route('/StartParallelJob/<int:value>/<int:count>')
class StartParallelJob(ResourceBase):
    @inject
    def __init__(self, job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service

    @TestParallelModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, value, count):
        run_date = datetime.now()
        ap_scheduler_job = self.job_operation_service.add_job_with_date(job_function=TestParallelScheduler.operation,
                                                                        run_date=run_date,
                                                                        args=(None, value, count,))
        result = JobSchedulerModels.get_ap_scheduler_job_model(ap_scheduler_job)
        return CommonModels.get_response(result=result)


class TestParallelScheduler:
    @staticmethod
    def operation(job_id, value, count):
        test_parallel_service = IocManager.injector.get(TestParallelService)
        result = test_parallel_service.test_performance_parallel(value, count)
        return CommonModels.get_response(message=result)
