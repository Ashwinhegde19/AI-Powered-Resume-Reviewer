from fastapi import FastAPI, UploadFile, Path, File
from .utils.file import save_to_disk
from .queue.q import q
from .db.collections.files import files_collection, FileSchema
from .queue.workers import process_file

from bson import ObjectId

app = FastAPI()


@app.get("/")
def hello():
    return {"status": "healthy"}


@app.get("/{id}")
async def get_file_by_id(id: str = Path(..., description="ID of the file")):
    db_file = await files_collection.find_one({"_id": ObjectId(id)})

    print(db_file)

    return {
        "_id": str(db_file["_id"]),
        "name": db_file["name"],
        "status": db_file["status"],
        "result": db_file["result"] if "result" in db_file else None,
    }


@app.post("/upload")
async def upload_file(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):

    db_file = await files_collection.insert_one(
        document=FileSchema(
            name=resume.filename,
            status="saving",
            resume_path="",
            jd_path="",
            rewritten_jd=None,
            strengths=None,
            weaknesses=None,
            improvements=None,
            result=None
        )
    )
    base_path = f"/mnt/uploads/{str(db_file.inserted_id)}"
    resume_path = f"{base_path}/{resume.filename}"
    jd_path = f"{base_path}/{jd.filename}"

    await save_to_disk(file=await resume.read(), path=resume_path)
    await save_to_disk(file=await jd.read(), path=jd_path)

    await files_collection.update_one({"_id": db_file.inserted_id}, {
        "$set": {
            "resume_path": resume_path,
            "jd_path": jd_path,
            "status": "queued"
        }
    })

    q.enqueue(process_file, str(db_file.inserted_id), resume_path, jd_path)
    return {"file_id": str(db_file.inserted_id)}
