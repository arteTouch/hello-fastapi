from fastapi import APIRouter, Response, status, File, UploadFile
from typing import List
import os

uploads_router = APIRouter()

@uploads_router.post('/file')
def file(file: bytes = File()):
    return {'file_size': len(file)}

from fastapi import APIRouter, UploadFile, File, HTTPException, Response, status
import os

uploads_router = APIRouter()

@uploads_router.post('/file-upload')
def upload_file(response: Response, file: UploadFile = File(...)):
    folder_path = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    file_location = os.path.join(folder_path, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    response.status_code = status.HTTP_201_CREATED
    return {'filename': file.filename}

@uploads_router.post('/files-upload')
def upload_file(response: Response, files: List[UploadFile] = File(...)):
    folder_path = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    filename_list = []
    for file in files:
        file_location = os.path.join(folder_path, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        filename_list.append(file.filename)
    response.status_code = status.HTTP_201_CREATED
    return {'filename_list': filename_list}

