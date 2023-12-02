from fastapi import APIRouter, Response, status, Depends
from db.models import Category
from pymongo import MongoClient
from db import db_qry, alter_data


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'HELLO'

category_router = APIRouter()

@category_router.post('/create')
def post(response: Response, category: Category):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    category = dict(category)
    if db_qry.categories(db, category['name']) is None:
        alter_data.insert_category(db,category)
        response.status_code = status.HTTP_201_CREATED
        return True
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False

@category_router.get('/read/all')
def get(response: Response):
    response.status_code = status.HTTP_200_OK
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    cursor = db_qry.categories(db)
    category_list = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        category_list.append(doc)
    if len(category_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return category_list