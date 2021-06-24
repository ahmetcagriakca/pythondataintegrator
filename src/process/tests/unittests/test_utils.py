import os
from unittest import TestCase

from infrastructor.utils.Utils import Utils


class TestUtils(TestCase):

    def __init__(self, methodName='RunTestUtils'):
        super(TestUtils, self).__init__(methodName)
        pass

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_folders1(self):
        self.root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
        folders = Utils.find_sub_folders(self.root_directory + '\\models\\dao')
        module_list, module_attr_list = Utils.get_modules(folders)
        for module in module_list:
            print(module)
