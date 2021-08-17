import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate


from db import db
from resources.user import UserRegister, Login, FetchUser, TokenRefresh
from resources.image import ImageResource , ImageDelete


app = Flask(__name__)
app.secret_key = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(Login, '/login')
api.add_resource(FetchUser, '/fetchuser')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ImageResource, '/uploadimage')
api.add_resource(ImageDelete, '/uploadimage/delete/<int:img_id>')


if __name__ == '__main__':
    db.init_app(app)
    # migrate = Migrate(app, db)
    app.run(debug=True)
