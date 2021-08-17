import datetime

from db import db


class ImageModel(db.Model):
    __tablename__ = "Image-Upload"
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(60), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, image_path: str, user_email: str):
        self.image_path = image_path
        self.user_email = user_email

    def json(self):
        return {
            "image_name": self.image_path,
            "user_email": self.user_email
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_by_email(cls, email: str):
        return cls.query.filter_by(user_email=email).all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()