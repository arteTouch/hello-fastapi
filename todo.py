from fastapi import APIRouter, Response, status
from models import Task

todo_router = APIRouter()

todo_list = []

@todo_router.post('/create')
def post(response: Response, task: Task):
    response.status_code = status.HTTP_201_CREATED
    for todo in todo_list:
        if todo.id == task.id:
            response.status_code = status.HTTP_409_CONFLICT
            return {'Error': 'Task with this id already exists'}
    todo_list.append(task)
    return {'todo_list': todo_list}

@todo_router.get('/read/all')
def get(response: Response):
    response.status_code = status.HTTP_200_OK
    if len(todo_list) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return 'There are no elements'
    return {'todo_list': todo_list}

@todo_router.put('/update/{id}')
def put(response: Response, id: int, task: Task):
    response.status_code = status.HTTP_404_NOT_FOUND
    if id < len(todo_list):
        response.status_code = status.HTTP_200_OK
        todo_list[id] = task
        return {'todo_list': todo_list}
    return 'Task with this id does not exists'

@todo_router.delete('/delete/{id}')
def delete(response: Response, id: int):
    response.status_code = status.HTTP_404_NOT_FOUND
    if id < len(todo_list):
        response.status_code = status.HTTP_200_OK
        del todo_list[id]
        return {'todo_list': todo_list}
    return 'Task with this id does not exists'
 