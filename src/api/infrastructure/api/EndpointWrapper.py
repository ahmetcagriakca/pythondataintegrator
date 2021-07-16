import json
import traceback
from abc import ABC
from datetime import datetime
import inspect
import typing
from flask import request
from flask_restx import fields, inputs
from flask_restx.reqparse import RequestParser, Argument

from IocManager import IocManager
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter
from infrastructure.api.utils.TypeChecker import TypeChecker
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.exceptions.OperationalException import OperationalException
from infrastructure.json.JsonConvert import JsonConvert
from infrastructure.logging.SqlLogger import SqlLogger

T = typing.TypeVar('T')


class EndpointWrapper:
    BaseModel = IocManager.api.model('BaseModel', {
        'IsSuccess': fields.Boolean(description='Is Success', default=True),
        'Message': fields.String(description='Message', default="Operation Completed"),
        'Result': fields.Raw(description='Service result values'),
    })

    @staticmethod
    def date_converter(o):
        if isinstance(o, datetime):
            return o.isoformat()

    @staticmethod
    def get_response(result=None, message=None):
        return {'Result': result, 'Message': message}

    @staticmethod
    def get_error_response(message):
        return {"IsSuccess": False, 'Message': message}

    @staticmethod
    def annotation_resolver(annotations):
        generic_type_checker = TypeChecker()
        definition = {}
        for key in annotations:
            value = annotations[key]
            specified_value = None
            if value == int:
                specified_value = fields.Integer(description=f'{key}', default=None)
            elif value == str:
                specified_value = fields.String(description=f'{key}', default=None)
            elif value == bool:
                specified_value = fields.Boolean(description=f'{key}', default=None)
            elif value == datetime:
                specified_value = fields.DateTime(description=f'{key}', default=None,
                                                  example=(datetime.now().isoformat()))
                pass
            elif value == float:
                specified_value = fields.Float(description=f'{key}', default=None)
                pass
            else:

                if generic_type_checker.is_generic(value):
                    nested_annotations = value.__args__[0]().__annotations__
                    nested_model_definition = EndpointWrapper.annotation_resolver(nested_annotations)
                    nested_model = IocManager.api.model(value.__args__[0].__name__, nested_model_definition)
                    specified_value = fields.List(fields.Nested(nested_model), description=f'')
                elif generic_type_checker.is_base_generic(value):
                    #TODO:Base generic class
                    print('value type should be a structure of', value.__args__[0])
                elif inspect.isclass(value):
                    nested_annotations = value().__annotations__
                    nested_model_definition = EndpointWrapper.annotation_resolver(nested_annotations)
                    nested_model = IocManager.api.model(value.__name__, nested_model_definition)
                    specified_value = fields.Nested(nested_model, description=f'')
                else:
                    print('Type not know', value)
            if specified_value is not None:
                definition[key] = specified_value
        return definition

    @staticmethod
    def request_model(model_type: typing.Type[T]) -> RequestParser:
        instance = model_type()
        annotations = instance.__annotations__

        model_definition = EndpointWrapper.annotation_resolver(annotations)
        model = IocManager.api.model(model_type.__name__, model_definition)
        return model

    @staticmethod
    def response_model(model_type: typing.Type[T]) -> RequestParser:
        instance = model_type()
        annotations = instance.__annotations__

        model_definition = EndpointWrapper.annotation_resolver(annotations)
        model = IocManager.api.model(model_type.__name__, model_definition)
        success_model = IocManager.api.model(model_type.__name__ + 'Base', {
            'IsSuccess': fields.Boolean(description='Is Success', default=True),
            'Message': fields.String(description='Message', default="Operation Completed"),
            'Result': fields.Nested(model, description='Result'),
        })
        return success_model

    @staticmethod
    def create_parser(name, input_type: typing.Type[T]) -> RequestParser:
        parser: RequestParser = IocManager.api.parser()
        parser.add_argument(EndpointWrapper.create_argument(name=name, type=input_type, location='form', help=name))
        return parser

    @staticmethod
    def get_request_from_parser_for_primitive(name,input_type: typing.Type[T]) -> T:
        parser = EndpointWrapper.create_parser(name=name,input_type=input_type)
        data = parser.parse_args(request)
        # req: T = JsonConvert.FromJSON(json.dumps(data))
        return data[name]

    @staticmethod
    def create_argument(name, type, location, help) -> Argument:
        specified_type = type
        if type == bool:
            specified_type = inputs.boolean
        argument = Argument(name, type=specified_type, location=location, help=help)
        return argument

    @staticmethod
    def request_parser(parser_type: typing.Type[T]) -> RequestParser:
        parser: RequestParser = IocManager.api.parser()
        instance = parser_type()
        if isinstance(instance, PagingParameter):
            parser.add_argument('PageNumber', type=int, location='args', help='Page Number')
            parser.add_argument('PageSize', type=int, location='args', help='Page Size')
        if isinstance(instance, OrderByParameter):
            parser.add_argument('OrderBy', type=str, location='args', help='Order By')
            parser.add_argument('Order', type=str, location='args', help='Order')
        annotations = instance.__annotations__

        for name in annotations:
            value = annotations[name]
            parser.add_argument(EndpointWrapper.create_argument(name=name, type=value, location='args', help=name))
        return parser


    @staticmethod
    def get_request_from_parser(parser_type: typing.Type[T]) -> T:
        data = EndpointWrapper.request_parser(parser_type).parse_args(request)
        req: T = JsonConvert.FromJSON(json.dumps(data))
        return req

    @staticmethod
    def get_request_from_body(parser_type: typing.Type[T]) -> T:
        data = IocManager.api.payload
        req: T = JsonConvert.FromJSON(json.dumps(data))
        return req
