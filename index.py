# Crear un servidor sencillo
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults
from dotenv import load_dotenv
import os

load_dotenv()

SCHEMA = os.environ.get('SCHEMA')
PORT = int(os.environ.get('PORT'))
HOST = os.environ.get('HOST')

# Our libraries
from api.http.response import Response as res
from api.http.request import Request

# Urls
from api.components.user.urls import Urls as user_urls
from api.components.todo.urls import Urls as todo_urls

# Dentro de env están los headers, protocolos, queryset y params
# start_response es un callback, el primer argumento es el status y el segundo las cabeceras
# En el return devolvemos la info que queremos mostrar al usuario, un string en utf-8
def api(env, start_response):


    try:
        req = Request(env)

        # Add routers
        req.add_routers(user_urls.load_routes(req, start_response))
        req.add_routers(todo_urls.load_routes(req, start_response))

        return req.send(start_response)
    except Exception as e:
        print(e)
        message = 'Internal Server Error'
        code = res.HTTP_INTERNAL_SERVER_ERROR

        if isinstance(e.args[0], dict):
            if 'message' in e.args[0]:
                message = e.args[0]['message']
            if 'code' in e.args[0]:
                code = e.args[0]['code']

        return res.error(start_response, message, code=code)

    # return res.success(start_response, req.input_params, code=res.HTTP_STATUS_OK)

    # status = '200 OK'
    # headers = [('Content-type', 'text/plain; charset=utf-8')]

    # start_response(status, headers)

    # ret = [("%s: %s\n" % (key, value)).encode("utf-8") for key, value in env.items()]
    # # response_data = {key: value for key, value in env.items()}
    # return ret

# el primer parámetro es la url, en nuestro caso localhost
# El segundo es el puerto
# El tercerlo es la función que se encargará de gestionar todas las llamadas a nuestro server
print(f'Server listen in {SCHEMA}://{HOST}:{PORT}')
server = make_server(HOST, PORT, api)

# Esto hace que el servidor se quede a la escucha por siempre hasta que nosotros lo cerremos
server.serve_forever()