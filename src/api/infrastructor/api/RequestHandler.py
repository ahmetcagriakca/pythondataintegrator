from flask import request, Response

from IocManager import IocManager
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from models.configs.ApiConfig import ApiConfig


class RequestHandlers:
    @staticmethod
    def set_headers(response):
        api_config: ApiConfig = IocManager.config_manager.get(ApiConfig)
        white_origin = None
        if api_config.origins is not None:
            white_origin = api_config.origins.split(',')
        if (white_origin is not None and ((len(white_origin) == 1 and white_origin[0] == '*') or (
        ('Origin' in request.headers and request.headers['Origin'] in white_origin)))):
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
            # response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Server'] = ''
        return response

    @staticmethod
    def after_request(response:Response):
        response = RequestHandlers.set_headers(response=response)
        IocManager.injector.get(DatabaseSessionManager).close()
        return response
