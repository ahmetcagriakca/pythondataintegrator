from flask_restplus import fields
from flask_restplus.reqparse import RequestParser

from infrastructor.IocManager import IocManager


class TestParallelModels:
    ns = IocManager.api.namespace('TestParallel', description='Test endpoints for api call', path='/api/TestParallel')


