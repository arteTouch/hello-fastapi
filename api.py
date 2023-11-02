from fastapi import FastAPI, APIRouter, Query
from todo import todo_router
from upload_router import uploads_router

app = FastAPI()
router = APIRouter()

@router.get('/page')
def page(pg: int=Query(1, gt=1, lt=20), size: int=Query(5, ge=5, le=20)):
    return {'page': pg, 'size': size}

app.include_router(router)
app.include_router(todo_router, prefix='/todos')
app.include_router(uploads_router, prefix='/uploads')