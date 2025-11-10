from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from bson import ObjectId
from schemas import Attendance, Marks, Timetable, User
from database import create_document, get_documents

app = FastAPI(title="Academic Tracker API")

# Allow frontend to call the API from a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Utils ----------

def _serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(doc, dict):
        return doc
    d = dict(doc)
    _id = d.get("_id")
    if isinstance(_id, ObjectId):
        d["_id"] = str(_id)
    return d


def _serialize_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [_serialize_doc(d) for d in docs]


# ---------- Models for seeding ----------

class SeedAttendanceBody(BaseModel):
    items: List[Attendance]

class SeedMarksBody(BaseModel):
    items: List[Marks]

class SeedTimetableBody(BaseModel):
    item: Timetable

class SeedUserBody(BaseModel):
    item: User


# ---------- Basic health ----------

@app.get("/")
def root():
    return {"message": "Academic Tracker API running"}


@app.get("/test")
def test():
    # Simple health check; database usage is optional at runtime
    return {"status": "ok"}


# ---------- Seed routes ----------

@app.post("/seed/attendance")
def seed_attendance(body: SeedAttendanceBody):
    count = 0
    for item in body.items:
        # use model_dump for pydantic v2
        create_document("attendance", item.model_dump())
        count += 1
    return {"inserted": count}


@app.post("/seed/marks")
def seed_marks(body: SeedMarksBody):
    count = 0
    for item in body.items:
        create_document("marks", item.model_dump())
        count += 1
    return {"inserted": count}


@app.post("/seed/timetable")
def seed_timetable(body: SeedTimetableBody):
    create_document("timetable", body.item.model_dump())
    return {"inserted": 1}


@app.post("/seed/user")
def seed_user(body: SeedUserBody):
    create_document("user", body.item.model_dump())
    return {"inserted": 1}


# ---------- Data routes ----------

@app.get("/attendance")
def get_attendance():
    try:
        docs = get_documents("attendance", {}, 100)
        return _serialize_list(docs)
    except Exception:
        # Return empty list if database isn't configured
        return []


@app.get("/marks")
def get_marks():
    try:
        docs = get_documents("marks", {}, 100)
        return _serialize_list(docs)
    except Exception:
        return []


@app.get("/timetable")
def get_timetable():
    try:
        docs = get_documents("timetable", {}, 1)
        if not docs:
            return {"data": {}}
        return _serialize_doc(docs[0])
    except Exception:
        return {"data": {}}


@app.get("/user")
def get_user():
    try:
        docs = get_documents("user", {}, 1)
        return _serialize_doc(docs[0]) if docs else {}
    except Exception:
        return {}