from flask_restplus import fields
from flask_restplus.reqparse import RequestParser

from infrastructor.IocManager import IocManager


class TestModels:
    ns = IocManager.api.namespace('Test', description='Test endpoints for api call', path='/api/Test')

    parser: RequestParser = IocManager.api.parser()
    parser.add_argument('value', type=int, location='args', help='Queried value')
    parser.add_argument('value_for_sum', type=int, location='args', help='Queried value')

    sum_model = IocManager.api.model('SumModel', {
        'value': fields.Integer,
        'value_for_sum': fields.Integer
    })

    mssql_model = IocManager.api.model('MssqlModel', {
        'HOST': fields.String,
        'DATABASE': fields.String,
        'USER': fields.String,
        'PASSWORD': fields.String,
    })
    oracle_model = IocManager.api.model('OracleModel', {
        'HOST': fields.String,
        'PORT': fields.String,
        'DATABASE': fields.String,
        'USER': fields.String,
        'PASSWORD': fields.String,
    })

