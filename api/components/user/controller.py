from api.http.response import Response as res
from email_validator import validate_email, EmailNotValidError
from api.components.auth.controller import Controller as auth_controller


class Controller:

    TABLE = 'user'

    @classmethod
    def create_user(cls, req, start_response):

        if not 'email' in req.input_params or not 'password' in req.input_params:
            return res.error(start_response, 'You must send email and password for create an user', code=res.HTTP_BAD_REQUEST)

        email = req.input_params['email']
        password = req.input_params['password']

        try:
            valid = validate_email(email)

            email = valid.email
        except EmailNotValidError as e:
            return res.error(start_response, str(e), code=res.HTTP_BAD_REQUEST)

        insert = {
            'email': email
        }

        user_id = req.ddbb.insert_data(cls.TABLE, insert)

        if user_id is None:
            return res.error(start_response, 'Error to create user, please try it later')

        req.input_params['user_id'] = user_id

        return auth_controller.create_auth(req, start_response)