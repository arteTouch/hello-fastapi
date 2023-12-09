from fastapi import FastAPI, APIRouter, Query, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
from todo import todo_router
from upload_router import uploads_router
from user import user_router
from category import category_router
from fastapi.templating import Jinja2Templates
from db import db_qry
from pymongo import MongoClient
from db.db import get_db

templates = Jinja2Templates(directory='templates')

app = FastAPI()
router = APIRouter()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST'],
    allow_headers=[],
)

@app.middleware('http')
async def add_processing_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response.headers['X-Processing-Time'] = str(time.time() - start_time)
    return response

@router.get('/page/')
def index(request: Request, db: MongoClient = Depends(get_db)):
    todo_list = db_qry.todos(db)
    for todo in todo_list:
        todo['category_id'] = db_qry.categories(db, id=todo['category'])['_id']
        todo['category'] = db_qry.categories(db, id=todo['category'])['name']
    category_list = db_qry.categories(db)
    return templates.TemplateResponse('todo/index.html', {'request': request,
                                                          'todo_list': todo_list,
                                                          'category_list': category_list})

app.include_router(router)
app.include_router(todo_router, prefix='/todos')
app.include_router(uploads_router, prefix='/uploads')
app.include_router(user_router, prefix='/user')
app.include_router(category_router, prefix='/category')