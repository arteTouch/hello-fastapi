from fastapi import APIRouter, Body
from models import Task

todo_router = APIRouter()

todo_list = ['braekfast', 'lounch']

@todo_router.post('/')
def post(task: Task):
    todo_list.append(task)
    return {'todo_list': todo_list}

@todo_router.get('/')
def get():
    return {'todo_list': todo_list}

@todo_router.put('/{id}')
def put(id: int, task: Task):
    todo_list[id] = task
    return {'todo_list': todo_list}

@todo_router.delete('/{id}')
def delete(id: int):
    del todo_list[id]
    return {'todo_list': todo_list}
 