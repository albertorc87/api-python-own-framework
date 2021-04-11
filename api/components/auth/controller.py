from api.http.response import Response as res

import bcrypt

class Controller:

    TABLE = 'auth'

    @classmethod
    def create_auth(cls, req, start_response):

        password = req.input_params['password'].encode()

        insert = {
            'user_id': str(req.input_params['user_id']),
            'email': req.input_params['email'],
            'password': bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        }

        result = req.ddbb.insert_data(cls.TABLE, insert)

        del insert['password']

        if result:
            return res.success(start_response, insert, code=res.HTTP_CREATED)

        return res.error(start_response, 'Error to create user, please try it later')