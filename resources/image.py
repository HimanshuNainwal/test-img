import os
from typing import List, Dict
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required


from models.image import ImageModel
from models.users import UserModel
from common.utils import Utils


class ImageResource(Resource):

    @jwt_required(refresh=True)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=str, required=True, help="email field is required")
        data = parser.parse_args()

        if not data:
            return {"message": "Accept only json format"}, 401

        user = UserModel.find_by_email(get_jwt_identity())
        image_path = Utils.save_image(user.id, user.username, data['image'], "png")
        img = ImageModel(image_path, user.email)
        img.save_to_db()

        return {"status": "Image Uploaded"}, 201

    @jwt_required(refresh=True)
    def get(self):
        img = ImageModel.find_all_by_email(get_jwt_identity())
        if img is None:
            return {"message": "Currently no picture uploaded"}, 200
        decoded_string = {}

        try:
            for i in img:
                print(Utils.open_image(i.image_path))
                decoded_string[i.id] = (Utils.open_image(i.image_path))
            return decoded_string, 200

        except Exception as e:
            img_id = img[-1].id
            img_not_found = ImageModel.find_all_by_id(img_id)
            img_not_found.delete_from_db()
            return {"error": "File Not found in database"}



class ImageDelete(Resource):
    @jwt_required(refresh=True)
    def delete(self, img_id):

        image = ImageModel.find_by_id(img_id)

        if image is None:
            return{"Error": "Image not found"}
        if os.path.exists(image.image_path):
            os.remove(image.image_path)
        else:
            print("The file does not exist")
        image.delete_from_db()
        return {"Message": f"Image deleted With Id {image.id}"}


