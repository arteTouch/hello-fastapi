from fastapi import APIRouter, Response, status, Depends
from db.models import Task, User, Category
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing_extensions import Annotated
from db.db import get_db
from db import db_qry, alter_data
from modules import auth_tools


todo_router = APIRouter()

Token = Annotated[str, Depends(auth_tools.auth_shema)]
DB = Annotated[MongoClient, Depends(get_db)]

@todo_router.post('/create')
def post(response: Response, task: Task, db: DB):
    if db_qry.todos(db, task.name) is None:
        res = alter_data.insert_task(db, task)
        response.status_code = status.HTTP_201_CREATED
        return res.acknowledged
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False

@todo_router.get('/read/all')
def get(response: Response, token: Token, db: DB):
    user = auth_tools.verify_token(db, token)
    if user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    todo_list = db_qry.todos(db)
    if len(todo_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    response.status_code = status.HTTP_200_OK
    return todo_list

@todo_router.get('/read/{id}')
def get_one(response: Response, id: str, db: DB):
    res = db_qry.todos(db, id)
    if res is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
    res['_id'] = str(res['_id'])
    response.status_code = status.HTTP_200_OK
    return res
    
@todo_router.put('/update/{id}')
def put(response: Response, id: str, task: Task, db: DB):
    res = alter_data.update_task(db, id, task)
    response.status_code = status.HTTP_200_OK
    if not res.acknowledged:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res.acknowledged

@todo_router.put('/update-status/{id}')
def put(response: Response, id: str, db: DB):
    res = alter_data.update_status(db, id)
    response.status_code = status.HTTP_200_OK
    if not res.acknowledged:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res.acknowledged

@todo_router.delete('/delete/{id}')
def delete(response: Response, id: str, db: DB):
    res = alter_data.delete_task(db, id)
    response.status_code = status.HTTP_200_OK
    if not res.acknowledged:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return res.acknowledged
 