import json
import traceback
from datetime import datetime
import inspect
import typing
from flask import request
from flask_restx import fields, inputs
from flask_restx.reqparse import RequestParser, Argument

from IocManager import IocManager
from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.json.JsonConvert import JsonConvert
from infrastructor.logging.SqlLogger import SqlLogger

# python 3.7
if hasattr(typing, '_GenericAlias'):
    def _is_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            return True
        if isinstance(cls, typing._SpecialForm):
            return cls not in {typing.Any}
        return False


    def _is_base_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            if cls.__origin__ in {typing.Generic, typing._Protocol}:
                return False
            if isinstance(cls, typing._VariadicGenericAlias):
                return True
            return len(cls.__parameters__) > 0
        if isinstance(cls, typing._SpecialForm):
            return cls._name in {'ClassVar', 'Union', 'Optional'}
        return False
else:
    # python <3.7
    if hasattr(typing, '_Union'):
        # python 3.6
        def _is_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union, typing._Optional, typing._ClassVar)):
                return True
            return False


        def _is_base_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union)):
                return cls.__args__ in {None, ()}
            if isinstance(cls, typing._Optional):
                return True
            return False
    else:
        # python 3.5
        def _is_generic(cls):
            if isinstance(cls, (
                    typing.GenericMeta, typing.UnionMeta, typing.OptionalMeta, typing.CallableMeta, typing.TupleMeta)):
                return True
            return False


        def _is_base_generic(cls):
            if isinstance(cls, typing.GenericMeta):
                return all(isinstance(arg, typing.TypeVar) for arg in cls.__parameters__)
            if isinstance(cls, typing.UnionMeta):
                return cls.__union_params__ is None
            if isinstance(cls, typing.TupleMeta):
                return cls.__tuple_params__ is None
            if isinstance(cls, typing.CallableMeta):
                return cls.__args__ is None
            if isinstance(cls, typing.OptionalMeta):
                return True
            return False


        def is_generic(cls):
            """
            Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
            Union and Tuple - anything that's subscriptable, basically.
            """
            return _is_generic(cls)


        def is_base_generic(cls):
            """
            Detects generic base classes, for example `List` (but not `List[int]`)
            """
            return _is_base_generic(cls)


        def is_qualified_generic(cls):
            """
            Detects generics with arguments, for example `List[int]` (but not `List`)
            """
            return is_generic(cls) and not is_base_generic(cls)


@IocManager.api.errorhandler(OperationalException)
def handle_operational_exception(exception):
    separator = '|'
    default_content_type = "application/json"
    mime_type_string = "mimetype"
    """Return JSON instead of HTML for HTTP errors."""
    IocManager.injector.get(RepositoryProvider).rollback()
    # start with the correct headers and status code from the error
    exception_traceback = traceback.format_exc()
    output = separator.join(exception.args)
    # replace the body with JSON
    # response = json.dumps()
    output_message = "empty"
    if output is not None and output != "":
        output_message = output
    trace_message = "empty"
    if exception_traceback is not None and exception_traceback != "":
        trace_message = exception_traceback
    IocManager.injector.get(SqlLogger).error(f'Operational Exception Messsage:{output_message} - Trace:{trace_message}')
    return {
               "result": "",
               "isSuccess": "false",
               "message": output
           }, 400, {mime_type_string: default_content_type}


T = typing.TypeVar('T')


class CommonModels:
    SuccessModel = IocManager.api.model('SuccessModel', {
        'IsSuccess': fields.Boolean(description='Service finished operation with successfully', default=True),
        'Message': fields.String(description='Service result values', default="Operation Completed"),
        'Result': fields.Raw(description='Service result values'),
    })

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
    def api_model(model_type: typing.Type[T]) -> RequestParser:
        instance = model_type()
        annotations = instance.__annotations__

        def annotation_resolver(annotations):
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
                elif value == float:
                    specified_value = fields.Float(description=f'{key}', default=None)
                    pass
                else:

                    if _is_generic(value):
                        nested_annotations = value.__args__[0]().__annotations__
                        nested_model_definition = annotation_resolver(nested_annotations)
                        nested_model = IocManager.api.model(value.__args__[0].__name__, nested_model_definition)
                        specified_value = fields.List(fields.Nested(nested_model), description=f'')
                    elif _is_base_generic(value):
                        print('value type should be a structure of', value.__args__[0])
                    elif inspect.isclass(value):
                        nested_annotations = value().__annotations__
                        nested_model_definition = annotation_resolver(nested_annotations)
                        nested_model = IocManager.api.model(value.__name__, nested_model_definition)
                        specified_value = fields.Nested(nested_model, description=f'')
                    else:
                        print('Type not know', value)
                if specified_value is not None:
                    definition[key] = specified_value
            return definition

        model_definition = annotation_resolver(annotations)
        model = IocManager.api.model(model_type.__name__, model_definition)
        success_model = IocManager.api.model(model_type.__name__+'Base', {
            'IsSuccess': fields.Boolean(description='Is Success', default=True),
            'Message': fields.String(description='Message', default="Operation Completed"),
            'Result': fields.Nested(model, description='Result'),
        })
        return success_model

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

        def annotation_resolver(name, type, location, help) -> Argument:
            specified_type = type
            if type == bool:
                specified_type = inputs.boolean
            argument = Argument(name, type=specified_type, location=location, help=help)
            return argument

        for key in annotations:
            value = annotations[key]
            parser.add_argument(annotation_resolver(name=key, type=value, location='args', help=key))
        return parser

    @staticmethod
    def get_request_from_parser(parser_type: typing.Type[T]) -> T:
        data = CommonModels.request_parser(parser_type).parse_args(request)
        req: T = JsonConvert.FromJSON(json.dumps(data))
        return req

    @staticmethod
    def get_request_from_body(parser_type: typing.Type[T]) -> T:
        data = IocManager.api.payload
        req: T = JsonConvert.FromJSON(json.dumps(data))
        return req

class EntityModel:
    def __init__(self,
                 Id: int = None,
                 ):
        self.Id: int = Id
