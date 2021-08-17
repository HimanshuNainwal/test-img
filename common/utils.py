import base64
import os
from flask import current_app
from PIL import Image
from io import BytesIO
from passlib.hash import pbkdf2_sha512



class Utils:

    @staticmethod
    def save_image(user_id: str, username: str, image: str, extension: str) -> str:
        folder = f"{current_app.root_path}\\static\\user\\user_{user_id}"
        if not os.path.exists(folder):
            os.makedirs(folder)

        lists = os.listdir(folder)  # opening dir and listing them
        number_files = len(lists)  # then counting files

        image_name = f"{username}_{number_files + 1}"
        im = Image.open(BytesIO(base64.b64decode(image)))
        im.save(f"{folder}\\{image_name}.{extension}", f"{extension.upper()}")
        return f"{folder}\\{image_name}.{extension}"

    @staticmethod
    def open_image(path: str) -> str:
        with open(rf"{path}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("UTF-8")

    @staticmethod
    def hash_password(password) -> str:
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def verify_password(password, hash_pass) -> bool:
        return pbkdf2_sha512.verify(password, hash_pass)

