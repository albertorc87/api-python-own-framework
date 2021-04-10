import re
from exceptions.url_exception import UrlException

class Router:

    # Allowed methods
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_PATCH = 'PATCH'
    METHOD_DELETE = 'DELETE'

    # Route list
    get_routes = {}
    post_routes = {}
    put_routes = {}
    patch_routes = {}
    delete_routes = {}

    def __init__(self):
        pass


    def get(self, route, callback):
        if route in self.get_routes:
            raise ValueError(f'Duplicate route {route}')

        self.get_routes[route] = callback


    def post(self, route, callback):
        if route in self.post_routes:
            raise ValueError(f'Duplicate route {route}')

        self.post_routes[route] = callback


    def put(self, route, callback):
        if route in self.put_routes:
            raise ValueError(f'Duplicate route {route}')

        self.put_routes[route] = callback


    def patch(self, route, callback):
        if route in self.patch_routes:
            raise ValueError(f'Duplicate route {route}')

        self.patch_routes[route] = callback


    def delete(self, route, callback):
        if route in self.delete_routes:
            raise ValueError(f'Duplicate route {route}')

        self.delete_routes[route] = callback


    def send(self, req, start_response):

        if req.request_method == self.METHOD_GET and len(self.get_routes) > 0:
            for route, callback in self.get_routes.items():

                route_regex, valid_keys = self.format_route(route)
                matches = re.finditer(route_regex, req.path)

                has_match = False
                for matchNum, match in enumerate(matches, start=1):
                    if len(valid_keys) > 0:
                        for param_key in valid_keys:
                            try:
                                req.url_params[param_key] = match[param_key]
                            except:
                                continue

                    has_match = True

                if has_match:
                    return callback(req, start_response)

        raise UrlException



    def format_route(self, route):

        regex = r"\{(?P<key>[^:].+?):(?P<type>(int|str))\}"
        matches = re.finditer(regex, route)
        valid_keys = []

        split_path = route.split('/')

        route_regex = '^'

        for sec_path in split_path:

            if sec_path == '':
                continue

            route_regex = route_regex + '\/'

            matches = re.finditer(regex, sec_path)

            if matches:
                for matchNum, match in enumerate(matches, start=1):

                    if match['type'] == 'int':
                        create_key = f'(?P<{match["key"]}>[0-9]+)'
                    else:
                        create_key = f'(?P<{match["key"]}>[a-zA-Z]+)'

                    sec_path = sec_path.replace(match[0], create_key)
                    # El id o lo que sea, nos hará falta en el match
                    valid_keys.append(match["key"])

            route_regex = route_regex + sec_path

        # Si es el index sin slash se lo añadimos nosotros para que lo encuentre
        if route_regex == '^':
            route_regex = '^\/'

        return f'{route_regex}$', valid_keys