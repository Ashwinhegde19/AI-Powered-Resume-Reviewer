from fastapi import FastAPI, UploadFile
from uuid import uuid4
from .utils.file import save_to_disk


app = FastAPI()


@app.get("/")
def hello():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_file(
    file: UploadFile

):
    id = uuid4()
    file_path = f"/mnt/uploads/{id}/{file.filename}"
    await save_to_disk(file=await file.read(), path=file_path)
    return {"file_id": id}