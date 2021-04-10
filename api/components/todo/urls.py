from api.http.response import Response as res

class Urls:

    @staticmethod
    def load_routes(req, start_response):

        req.router.get(
            '/todo/{id:int}',
            lambda req, start_response: res.success(start_response, {'index': '/todo/{id:int}'}, code=res.HTTP_STATUS_OK)
        )


        req.router.get(
            '/todo/test/{id:int}/{data:str}',
            lambda req, start_response: res.success(start_response, {'index': '/todo/test/{id:int}/{data:str}'}, code=res.HTTP_STATUS_OK)
        )

        req.router.get(
            '/todo',
            lambda req, start_response: res.success(start_response, {'index': '/todo'}, code=res.HTTP_STATUS_OK)
        )

        # res = router.send(req, start_response)
        # if res == None:
        #     pass
        # return router