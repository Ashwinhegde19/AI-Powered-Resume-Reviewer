from pydantic import Field
from typing import TypedDict, Optional
from pymongo.asynchronous.collection import AsyncCollection
from ..db import database


class FileSchema(TypedDict):
    name: str = Field(..., description="Name of the file")
    status: str = Field(..., description="Status of the file")
    resume_path: str = Field(..., description="Path to the resume")
    jd_path: str = Field(..., description="Path to the job description")
    rewritten_jd: Optional[str] = Field(None, description="Rewritten job description")
    strengths: Optional[str] = Field(None, description="Strengths identified")
    weaknesses: Optional[str] = Field(None, description="Weaknesses identified")
    improvements: Optional[str] = Field(None, description="Suggested improvements")
    result: Optional[str] = Field(None, description="The result from AI")


COLLECTION_NAME = "files"
files_collection: AsyncCollection = database[COLLECTION_NAME]
