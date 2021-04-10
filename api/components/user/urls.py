from api.http.response import Response as res

class Urls:

    @staticmethod
    def load_routes(req, start_response):

        req.router.get(
            '/user/{id:int}',
            lambda req, start_response: res.success(start_response, {'index': '/user/{id:int}'}, code=res.HTTP_STATUS_OK)
        )


        req.router.get(
            '/user/test/{id:int}/{data:str}',
            lambda req, start_response: res.success(start_response, {'index': '/user/test/{id:int}/{data:str}'}, code=res.HTTP_STATUS_OK)
        )

        req.router.get(
            '/user',
            lambda req, start_response: res.success(start_response, {'index': '/user'}, code=res.HTTP_STATUS_OK)
        )

        # res = router.send(req, start_response)
        # if res == None:
        #     pass
        # return router