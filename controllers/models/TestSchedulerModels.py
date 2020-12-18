from datetime import datetime, timedelta

from flask_restplus import fields
from flask_restplus.reqparse import RequestParser
from tzlocal import get_localzone

from infrastructor.IocManager import IocManager


class TestSchedulerModels:
    ns = IocManager.api.namespace('TestScheduler', description='Scheduler test endpoints', path='/api/TestScheduler')

    cron_sum_model = IocManager.api.model('CronSumModel', {
        'Cron': fields.String(description="Job cron value. ", required=True, example='*/1 * * * *'),
        'StartDate': fields.DateTime(
            description="Job start date. The start date for the job can be entered if necessary.", required=False,
            example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')),
        'EndDate': fields.DateTime(
            description="Job End date. The end date for the job can be entered if necessary.", required=False,
            example=(datetime.now() + timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
        'value': fields.Integer,
        'value_for_sum': fields.Integer
    })
    sum_model = IocManager.api.model('SumModel', {
        'RunDate': fields.DateTime(example=(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')),
        'value': fields.Integer,
        'value_for_sum': fields.Integer
    })
