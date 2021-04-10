# Standard: https://github.com/omniti-labs/jsend

import json

class Response:
    # Success code
    HTTP_STATUS_OK = '200 OK'

    # Client errors
    HTTP_BAD_REQUEST = '400 Bad Request'
    HTTP_UNAUTHORIZED = '401 Unauthorized'
    HTTP_FORBIDDEN = '403 Forbidden'
    HTTP_NOT_FOUND = '404 Not Found'

    # Server errors
    HTTP_INTERNAL_SERVER_ERROR = '500 Internal Server Error'


    @classmethod
    def success(cls, response, data, code = HTTP_STATUS_OK):

        cls.validate_status_code(code)

        headers = [('Content-Type', 'text/json')]
        response(code, headers)

        response_data = json.dumps({
            'status': 'success',
            'data': data
        })

        return [bytes(response_data, 'utf-8')]


    @classmethod
    def error(cls, response, message, is_fail = False, code = HTTP_INTERNAL_SERVER_ERROR):

        cls.validate_status_code(code)
        headers = [('Content-Type', 'text/json')]
        response(code, headers)

        status = 'error'

        if is_fail:
            status = 'fail'

        response_data = json.dumps({
            'status': status,
            'code': code,
            'message': message
        })

        return [bytes(response_data, 'utf-8')]


    @classmethod
    def validate_status_code(cls, code):
        valid_headers = [value for name, value in vars(cls).items() if name.startswith('HTTP_')]
        valid_headers.index(code)