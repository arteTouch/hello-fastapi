from fastapi import FastAPI, APIRouter, Query
from todo import todo_router

app = FastAPI()
router = APIRouter()

@router.get('/home')
def hello_world():
    return {'hello': 'world'}

@router.get('/page')
def page(pg: int=Query(1, gt=1, lt=20), size: int=Query(5, ge=5, le=20)):
    return {'page': pg, 'size': size}

app.include_router(router)
app.include_router(todo_router, prefix='/todos')