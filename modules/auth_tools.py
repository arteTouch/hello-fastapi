from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from db import db_qry


pwd_context = CryptContext(schemes=["bcrypt"])

secret = "secret"
algorithm = "HS256"
api_key_token = APIKeyHeader(name='Token')
auth_shema = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user) -> str:
    token = jwt.encode(user, secret, algorithm=algorithm)
    return token

def verify_token(db, token) -> dict:
    user_data = jwt.decode(token, secret, algorithms=algorithm)
    if user_data.get('name') is not None:
        user = db_qry.users(db, name=user_data['name'])
        return user
    return None

def authenticate_user(db, name: str, password: str) -> dict:
    user = db_qry.users(db, name=name)
    if user is None:
        return False
    if not verify_password(password, user['password']):
        return False
    return user