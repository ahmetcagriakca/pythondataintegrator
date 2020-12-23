from flask import request
from injector import inject

from controllers.common.models.CommonModels import CommonModels
from controllers.test.models.TestModels import TestModels
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase

@TestModels.ns.route('/path/<int:value>/<int:value_for_sum>', doc=False)
class TestResource(ResourceBase):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, value, value_for_sum):
        result = {'sum': value + value_for_sum}
        return CommonModels.get_response(result=result)


@TestModels.ns.route('/query', doc=False)
class TestResource(ResourceBase):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @TestModels.ns.expect(TestModels.parser, validate=True)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        data = TestModels.parser.parse_args(request)
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')  # This is FileStorage instance
        # url = do_something_with_file(uploaded_file)
        result = {'sum': value + value_for_sum}
        return CommonModels.get_response(result=result)

    @TestModels.ns.expect(TestModels.sum_model, validate=True)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        data = IocManager.api.payload
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')  # This is FileStorage instance
        result = {'sum': value + value_for_sum, "test": [{"test": 1}, {"test": 2}]}
        return CommonModels.get_response(result=result)

