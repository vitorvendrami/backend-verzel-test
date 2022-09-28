from app import db

from models.UserModel import Users


class UserService:
    """Class to handle users services"""

    @staticmethod
    def return_all_users():
        """Return all users"""

        usuarios_objetos = Users.query.all()
        usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

        return usuarios_json

    @staticmethod
    def return_user_by_id(id: int) -> Users:
        """Return user given it's id"""
        user = Users.query.filter_by(id=id).first()
        user_json_rpr = user.to_json() if user else {}

        return user_json_rpr

    @staticmethod
    def create_user(email: str, password: str, admin: bool) -> (bool, Users):
        """Creates a User"""
        try:
            user = Users(email=email, password=password, admin=admin)
            db.session.add(user)
            db.session.commit()
            return True, user.to_json()

        except Exception as e:
            return False, {}
