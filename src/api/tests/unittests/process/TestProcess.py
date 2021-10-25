from unittest import TestCase

import os

from pdip.dependency.container import DependencyContainer


class test_dynamic_call:
    def __init__(self, i):
        self.val = i

    def method_call_test(self, property1, property2=None):
        print(f"val:{self.val}")
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2


class TestProcess(TestCase):

    def __init__(self, methodName='TestProcess'):
        super(TestProcess, self).__init__(methodName)

        from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    @staticmethod
    def static_method_call_test(property1, property2=None):
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2

    def method_call_test(self, property1, property2=None):
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2
    @staticmethod
    def check_type(d):
        if d.dtype.name == 'datetime64[ns]':
            data=d.dt.to_pydatetime()
            return data
        else:
            data=d.values.tolist()
            return data

    def test_dynamic_static_method_call_with_args(self):
        # df = pd.DataFrame([{"a": 1, "b": "2011-10-20T00:00:00.000Z","c":'asd'}])
        df = df.astype(dtype={"a": "int", "b": "datetime64[ns]","c":"str"})
        # test = df.apply(self.check_type )
        #
        # # df.apply(lambda d: d.dt.to_pydatetime() if d.dtype.name =='datetime64[ns]' else d)
        # # df.dtypes
        # df.select_dtypes(include=['datetime64[ns]']).dtypes.name
        rows=[]
        for row in df.values.tolist():
            columns=[]
            for column in row:
                if column is not None and hasattr(column, 'to_pydatetime') :
                    columns.append(column.to_pydatetime())
                else:
                    columns.append(column)
            rows.append(columns)
        args = (3, 5,)
        method = self.static_method_call_test
        result = method(*args)
        assert result == 8

    def test_dynamic_static_method_call_with_kwargs(self):
        keyword_args = {
            "property2": 5,
            "property1": 3,
        }
        args = [self.static_method_call_test.__name__]
        result = getattr(type(self), args[0])(**keyword_args)
        assert result == 8

    def test_dynamic_method_call_with_kwargs(self):
        keyword_args = {
            "property2": 5,
            "property1": 3,
        }
        args = [test_dynamic_call.method_call_test.__name__]
        # method = getattr(test_dynamic_call, args[0])
        # result = method(test_dynamic_call, **keyword_args)

        instance=test_dynamic_call(i=1)
        result= instance.method_call_test(1,2)
        method = getattr(type(instance), args[0])
        result = method(instance, **keyword_args)
        assert result == 8
