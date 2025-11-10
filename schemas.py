from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Each Pydantic model corresponds to a MongoDB collection (lowercased class name)

class AttendanceItem(BaseModel):
    code: str
    title: str
    category: str
    faculty: str
    slot: str
    conducted: int
    absent: int
    percetage: str
    margin: int

class Attendance(BaseModel):
    # Will store one document per subject in the "attendance" collection
    code: str
    title: str
    category: str
    faculty: str
    slot: str
    conducted: int
    absent: int
    percetage: str
    margin: int

class MarkEntry(BaseModel):
    name: str
    mark: str
    total: str

class Marks(BaseModel):
    name: str
    code: str
    type: str
    marks: List[MarkEntry]
    credit: str
    total: Optional[str] = None

class Timetable(BaseModel):
    # Store the provided structure as-is
    data: Dict[str, Dict[str, Dict[str, Any]]]

class User(BaseModel):
    roll: str
    name: str
    program: str
    department: str
    specialisation: str
    semester: str
    batch: str
    section: str
