import inspect
import json
from functools import wraps

from infrastructure.api.EndpointWrapper import EndpointWrapper
from infrastructure.api.utils.TypeChecker import TypeChecker


class _Endpoint:
    def __init__(self, function, namespace=None):
        self.namespace = namespace
        self.function = function
        self.endpoint_wrapper = EndpointWrapper()

    def __call__(self, *args, **kwargs):
        input_type,input_name = self.find_input_type()

        if TypeChecker().is_class(input_type):
            if self.function.__name__ == 'get':
                req = self.endpoint_wrapper.get_request_from_parser(input_type)
            else:
                req = self.endpoint_wrapper.get_request_from_body(input_type)
        else:

            req = self.endpoint_wrapper.get_request_from_parser_for_primitive(input_name, input_type)

        res = self.function(args[0], req, **kwargs)

        if TypeChecker().is_class(input_type):
            result = json.loads(json.dumps(res.to_dict(), default=self.endpoint_wrapper.date_converter))
            return self.endpoint_wrapper.get_response(result=result)
        else:

            return self.endpoint_wrapper.get_response(message=res)


    # @wraps(fun)
    # @self.namespace.expect(expect_inputs(), validate=True)
    # @namespace.marshal_with(marshal_with_fields())
    def input_type_names(self):
        self.function.__annotations__.keys()
        return self.function.__annotations__.keys().remove("return")

    def input_types(self):
        input_annotations = self.function.__annotations__
        input_argument_types = []
        input_argument_names = []
        for annotation_key in input_annotations.keys():
            if annotation_key != "return":
                argument_type = input_annotations[annotation_key]
                input_argument_types.append(argument_type)
                input_argument_names.append(annotation_key)
        return input_argument_types, input_argument_names

    def return_type(self):
        if "return" in self.function.__annotations__:
            return self.function.__annotations__["return"]
        else:
            return None

    def find_input_type(self):
        input_types, input_names = self.input_types()
        if input_types == None or len(input_types) == 0:
            return None
        elif len(input_types) == 1:
            return input_types[0], input_names[0]
        else:
            return None

    def expect_inputs(self):
        input_type, input_name = self.find_input_type()

        if TypeChecker().is_class(input_type):
            if self.function.__name__ == 'get':
                expect_model = self.endpoint_wrapper.request_parser(input_type)
            else:
                expect_model = self.endpoint_wrapper.api_model(input_type)
        else:

            expect_model = self.endpoint_wrapper.create_parser(input_name, input_type)

        return expect_model

    def marshal_with_fields(self):
        if self.return_type() is None:
            fields = self.endpoint_wrapper.BaseModel
        else:
            fields = self.endpoint_wrapper.api_model(self.return_type())
        return fields


def endpoint(namespace):
    def decorator(function):
        def instance() -> _Endpoint:
            _instance = _Endpoint(function, namespace)
            return _instance

        @wraps(function)
        @namespace.expect(instance().expect_inputs(), validate=True)
        @namespace.marshal_with(instance().marshal_with_fields())
        def wrapper(*args, **kwargs):
            return instance().__call__(*args, **kwargs)

        return wrapper

    return decorator
