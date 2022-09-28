"""SET The Default Credentials to the database"""
import os

SECRET_KEY = "alura"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
    SGBD="mysql+mysqlconnector",
    usuario=os.environ.get("SQL_USER", default="root"),
    senha=os.environ.get("SQL_PASSWORD", default="password"),
    servidor=os.environ.get("SERVER", default="localhost"),
    database=os.environ.get("DATABASE", default="db"),
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
