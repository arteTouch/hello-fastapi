from fastapi import APIRouter, Response, status, Depends
from db.models import User
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordRequestForm
from db import db_qry, alter_data
from db.db import get_db
from modules import auth_tools
from todo import DB


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'HELLO'

user_router = APIRouter()


@user_router.post('/token')
def create_token(response: Response, db: DB, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_tools.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return False
    token = auth_tools.create_access_token(user)
    return {'access_token': token}
    

@user_router.post('/create')
def post(response: Response, user: User, db: DB):
    user = dict(user)
    if db_qry.users(db, user['name']) is None:
        user['password'] = auth_tools.get_password_hash(user['password'])
        alter_data.insert_user(db, user)
        response.status_code = status.HTTP_201_CREATED
        return True
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False

@user_router.get('/read/all')
def get(response: Response, db: DB):
    cursor = db_qry.users(db)
    user_list = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        user_list.append(doc)
    if len(user_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return user_list