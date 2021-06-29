from flask_restx.reqparse import RequestParser

from IocManager import IocManager


class PageModels:
    ns = IocManager.api.namespace('DataOperationJobPage', description='Job Page endpoints',
                                  path='/Job')

    parser: RequestParser = IocManager.api.parser()
    parser.add_argument('Page', type=int, location='args', help='Queried value')
    parser.add_argument('Limit', type=int, location='args', help='Queried value')
    parser.add_argument('Filter', type=str, location='args', help='Queried value')
