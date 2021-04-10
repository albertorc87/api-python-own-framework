
import json
from json.decoder import JSONDecodeError
from urllib.parse import parse_qs
from importlib.util import find_spec
from importlib import import_module

from api.http.response import Response as res
from classes.router import Router
from exceptions.url_exception import UrlException

import api.components as components

class Request:

    def __init__(self, env):
        self.path = env['PATH_INFO']
        self.query_string = env['QUERY_STRING']
        self.request_method = env['REQUEST_METHOD']
        self.url_params = {}
        self.router = Router()

        self.input_params = self.inputParams(env)


    def send(self, start_response):
        try:
            return self.router.send(self, start_response)

        except UrlException as err:
            err.args = ({
                'message': 'Invalid url ' + self.path,
                'code': res.HTTP_BAD_REQUEST
            },)
            raise

        except Exception as err:
            print(err)
            raise

        # return res.success(start_response, {'test': 'send'}, code=res.HTTP_STATUS_OK)

    def inputParams(self, env):
        if self.request_method == 'GET':
            return {}

        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        if request_body_size == 0:
            return {}

        request_body = env['wsgi.input'].read(request_body_size)

        try:
            return json.loads(request_body)
        except JSONDecodeError as err:
            err.args = ({
                'message': 'Invalid format post',
                'code': res.HTTP_BAD_REQUEST
            },)
            raise

    def add_routers(self, component_router):

        method_list = ['get', 'post', 'put', 'patch', 'delete']

        # for method in method_list:
        #     value_attr_list_routes = getattr(component_router, f'{method}_routes')
        #     value_attr_valid_methods = getattr(component_router, f'METHOD_{method.upper()}')
        #     if len(value_attr_list_routes) > 1:
        #         self.router.combine_routes(value_attr_list_routes, value_attr_valid_methods)
