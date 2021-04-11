
from api.components.user.controller import Controller as user_controller

class Urls:

    @staticmethod
    def load_routes(req, start_response):

        # Create user
        req.router.post(
            '/user',
            lambda req, start_response: user_controller.create_user(req, start_response)
        )

        # Get user by id
        req.router.get(
            '/user/{id:int}',
            lambda req, start_response: res.success(start_response, {'index': '/user/{id:int}'}, code=res.HTTP_STATUS_OK)
        )

        # Get all users
        req.router.get(
            '/user',
            lambda req, start_response: res.success(start_response, {'index': '/user'}, code=res.HTTP_STATUS_OK)
        )

        # res = router.send(req, start_response)
        # if res == None:
        #     pass
        # return router