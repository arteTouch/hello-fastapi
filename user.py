from fastapi import APIRouter, Response, status, Depends
from db.models import User
from pymongo import MongoClient
from db import db_qry, alter_data


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'HELLO'

user_router = APIRouter()

@user_router.post('/create')
def post(response: Response, user: User):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    user = dict(user)
    if db_qry.users(db, user['name']) is None:
        alter_data.insert_user(db, user)
        response.status_code = status.HTTP_201_CREATED
        return True
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False

@user_router.get('/read/all')
def get(response: Response):
    response.status_code = status.HTTP_200_OK
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
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