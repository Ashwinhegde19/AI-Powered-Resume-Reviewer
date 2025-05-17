from fastapi import FastAPI, UploadFile
from uuid import uuid4

app = FastAPI()


@app.get("/")
def hello():
    return {"status": "healthy"}


@app.post("/upload")
def upload_file( 
    file: UploadFile

):
    id: uuid4()
    
    file_path = f"mnt/uploads/{id}/{file.filename}"
    
    