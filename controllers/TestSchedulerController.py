from datetime import datetime
from injector import inject
from controllers.models.CommonModels import CommonModels
from controllers.models.JobSchedulerModels import JobSchedulerModels
from controllers.models.TestSchedulerModels import TestSchedulerModels
from domain.pdi.services.JobOperationService import JobOperationService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.aps.ApSchedulerEvent import ApSchedulerEvent


@TestSchedulerModels.ns.route('/StartWithCron')
class TestResource(ResourceBase):
    @inject
    def __init__(self, job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service

    @TestSchedulerModels.ns.expect(TestSchedulerModels.cron_sum_model, validate=True)
    @TestSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        data = IocManager.api.payload
        start_date = data.get('StartDate')  #
        end_date = data.get('EndDate')  #
        cron = data.get('Cron')  #
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')
        ap_scheduler_job = self.job_operation_service.add_job_with_cron(job_function=TestScheduler.sum, cron=cron,
                                                                        start_date=start_date,
                                                                        end_date=end_date, args=(None,value, value_for_sum))
        result = JobSchedulerModels.get_ap_scheduler_job_model(ap_scheduler_job)
        return CommonModels.get_response(result=result)


@TestSchedulerModels.ns.route('/StartWithDate')
class StartWithDate(ResourceBase):
    @inject
    def __init__(self, job_operation_service: JobOperationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_operation_service = job_operation_service

    @TestSchedulerModels.ns.expect(TestSchedulerModels.sum_model, validate=True)
    @TestSchedulerModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        data = IocManager.api.payload
        rune_date_string = data.get('RunDate')  #
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')
        if rune_date_string is None or rune_date_string == '':
            return CommonModels.get_error_response(message="RunDate Requeired")

        run_date = datetime.strptime(rune_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        ap_scheduler_job = self.job_operation_service.add_job_with_date(job_function=TestScheduler.sum,
                                                                        run_date=run_date,
                                                                        args=(None,value, value_for_sum,))
        result = JobSchedulerModels.get_ap_scheduler_job_model(ap_scheduler_job)
        return CommonModels.get_response(result=result)


class TestScheduler:
    @staticmethod
    def alarm(time):
        print('Alarm! This alarm was scheduled at %s.' % time)
        obj = ApSchedulerEvent(Code="12")
        return obj

    @staticmethod
    def tick(job_id):
        print('Tick! The time is: %s %d' % datetime.now(), job_id)
        return '2'

    @staticmethod
    def sum(job_id, value, value_for_sum):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f'{date} value={value}, value_for_sum:{value_for_sum}', job_id=job_id)
        return value + value_for_sum
