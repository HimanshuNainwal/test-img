from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required


from models.users import UserModel
from common.utils import Utils


class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required')
        parser.add_argument('email', type=str, required=True, help='email is required')
        parser.add_argument('password', type=str, required=True, help='password is required')
        data = parser.parse_args()
        user = UserModel(data['username'], data['email'], Utils.hash_password(data['password']))
        if user.find_by_email(user.email):
            return {"Message": "A user with this email already registered"}, 400
        user.save_to_db()
        return {"Message": "Created"}, 201


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="email field is required")
        parser.add_argument('password', type=str, required=True, help="password is required")
        data = parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        if not user:
            return {"Message": "No user Found"}, 401

        if not user:
            return {
                       "Message": "No user found"
                   }, 401

        if Utils.verify_password(data['password'], user.password):
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(user.email)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200
        return {"message": "Invalid Credentials"}, 401


class FetchUser(Resource):

    @jwt_required()
    def get(self):
        user = UserModel.find_by_email(get_jwt_identity())
        if not user:
            return {"message": "User not found "}, 401
        return user.json(), 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, 200


