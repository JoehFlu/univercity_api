from typing import List

import requests
from bson import ObjectId
from bson.errors import InvalidId
from faker import Faker
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from pymongo import ASCENDING, MongoClient
from pymongo.errors import DuplicateKeyError


MONGO_URL = "mongodb://mongo:27017"
MONGO_DB_NAME = "university_api"
CASTLEMOCK_BASE_URL = "http://castlemock:8080/castlemock/mock/rest/project/QXcx23/application"
CASTLEMOCK_TIMEOUT_SECONDS = 3

tags_metadata = [
    {
        "name": "Utility",
        "description": "🔧 Вспомогательные эндпоинты (seed, health, и т.д.)",
    },
    {
        "name": "Students",
        "description": "👩‍🎓 CRUD операции со студентами",
    },
    {
        "name": "Courses",
        "description": "📚 CRUD операции с курсами",
    },
    {
        "name": "Enrollments",
        "description": "📝 CRUD операции с записями студентов на курсы",
    },
    {
        "name": "CastleMock",
        "description": "🌤️ Пример обращения к внешнему (mock) API",
    },
]

app = FastAPI(
    title="University API",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

fake = Faker()
client = MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB_NAME]

students = db["students"]
courses = db["courses"]
enrollments = db["enrollments"]


class Student(BaseModel):
    name: str
    age: int
    email: EmailStr


class StudentOut(Student):
    id: str


class Course(BaseModel):
    title: str
    description: str


class CourseOut(Course):
    id: str


class Enrollment(BaseModel):
    student_id: str
    course_id: str


class EnrollmentOut(Enrollment):
    id: str


def ensure_indexes():
    students.create_index([("email", ASCENDING)], unique=True)
    courses.create_index([("title", ASCENDING)])
    enrollments.create_index([("student_id", ASCENDING), ("course_id", ASCENDING)], unique=True)


def parse_object_id(value: str, entity: str):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"Invalid {entity} id")


def to_out(doc, model):
    payload = {
        key: str(value) if isinstance(value, ObjectId) else value
        for key, value in doc.items()
        if key != "_id"
    }
    return model(id=str(doc["_id"]), **payload)


def call_castlemock(method: str, path: str, payload=None):
    url = f"{CASTLEMOCK_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.request(
            method,
            url,
            json=payload,
            timeout=CASTLEMOCK_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"CastleMock error: {e}")


@app.on_event("startup")
def startup_event():
    ensure_indexes()


@app.post("/students/", response_model=StudentOut, tags=["Students"])
def create_student(student: Student):
    if students.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        result = students.insert_one(student.model_dump())
        return to_out(students.find_one({"_id": result.inserted_id}), StudentOut)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")


@app.get("/students/", response_model=List[StudentOut], tags=["Students"])
def list_students():
    return [to_out(doc, StudentOut) for doc in students.find()]


@app.put("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def update_student(student_id: str, student: Student):
    object_id = parse_object_id(student_id, "student")
    try:
        result = students.update_one({"_id": object_id}, {"$set": student.model_dump()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        updated = students.find_one({"_id": object_id})
        return to_out(updated, StudentOut)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
def delete_student(student_id: str):
    object_id = parse_object_id(student_id, "student")
    result = students.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    enrollments.delete_many({"student_id": {"$in": [object_id, str(object_id)]}})
    return {"status": "deleted", "entity": "student", "id": student_id}


@app.post("/courses/", response_model=CourseOut, tags=["Courses"])
def create_course(course: Course):
    result = courses.insert_one(course.model_dump())
    return to_out(courses.find_one({"_id": result.inserted_id}), CourseOut)


@app.get("/courses/", response_model=List[CourseOut], tags=["Courses"])
def list_courses():
    return [to_out(doc, CourseOut) for doc in courses.find()]


@app.put("/courses/{course_id}", response_model=CourseOut, tags=["Courses"])
def update_course(course_id: str, course: Course):
    object_id = parse_object_id(course_id, "course")
    result = courses.update_one({"_id": object_id}, {"$set": course.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    updated = courses.find_one({"_id": object_id})
    return to_out(updated, CourseOut)


@app.delete("/courses/{course_id}", status_code=status.HTTP_200_OK, tags=["Courses"])
def delete_course(course_id: str):
    object_id = parse_object_id(course_id, "course")
    result = courses.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollments.delete_many({"course_id": {"$in": [object_id, str(object_id)]}})
    return {"status": "deleted", "entity": "course", "id": course_id}


@app.post("/enrollments/", response_model=EnrollmentOut, tags=["Enrollments"])
def create_enrollment(enrollment: Enrollment):
    student_object_id = parse_object_id(enrollment.student_id, "student")
    course_object_id = parse_object_id(enrollment.course_id, "course")
    if not students.find_one({"_id": student_object_id}):
        raise HTTPException(status_code=404, detail="Student not found")
    if not courses.find_one({"_id": course_object_id}):
        raise HTTPException(status_code=404, detail="Course not found")
    try:
        result = enrollments.insert_one({
            "student_id": student_object_id,
            "course_id": course_object_id,
        })
        return to_out(enrollments.find_one({"_id": result.inserted_id}), EnrollmentOut)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Enrollment already exists")


@app.get("/enrollments/", response_model=List[EnrollmentOut], tags=["Enrollments"])
def list_enrollments():
    return [to_out(doc, EnrollmentOut) for doc in enrollments.find()]


@app.put("/enrollments/{enrollment_id}", response_model=EnrollmentOut, tags=["Enrollments"])
def update_enrollment(enrollment_id: str, enrollment: Enrollment):
    enrollment_object_id = parse_object_id(enrollment_id, "enrollment")
    student_object_id = parse_object_id(enrollment.student_id, "student")
    course_object_id = parse_object_id(enrollment.course_id, "course")
    if not students.find_one({"_id": student_object_id}):
        raise HTTPException(status_code=404, detail="Student not found")
    if not courses.find_one({"_id": course_object_id}):
        raise HTTPException(status_code=404, detail="Course not found")

    try:
        result = enrollments.update_one(
            {"_id": enrollment_object_id},
            {"$set": {"student_id": student_object_id, "course_id": course_object_id}},
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        updated = enrollments.find_one({"_id": enrollment_object_id})
        return to_out(updated, EnrollmentOut)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Enrollment already exists")


@app.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_200_OK, tags=["Enrollments"])
def delete_enrollment(enrollment_id: str):
    object_id = parse_object_id(enrollment_id, "enrollment")
    result = enrollments.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"status": "deleted", "entity": "enrollment", "id": enrollment_id}


@app.post("/seed/", tags=["Utility"])
def seed_data():
    students.delete_many({})
    courses.delete_many({})
    enrollments.delete_many({})
    fake.unique.clear()

    student_ids = [
        students.insert_one({
            "name": fake.name(),
            "age": fake.random_int(min=18, max=30),
            "email": fake.unique.email(),
        }).inserted_id
        for _ in range(5)
    ]

    course_ids = [
        courses.insert_one({
            "title": fake.job(),
            "description": fake.text(max_nb_chars=50),
        }).inserted_id
        for _ in range(3)
    ]

    for sid in student_ids:
        enrollments.insert_one({
            "student_id": sid,
            "course_id": fake.random_element(course_ids),
        })

    return {"message": "Database seeded successfully"}


@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}


@app.get("/external/weather", tags=["CastleMock"], summary="Get mock weather from CastleMock")
def get_mock_weather():
    return call_castlemock("GET", "x0T4QS/forecast")


@app.post("/external/auth/login", tags=["CastleMock"], summary="Mock user login via CastleMock")
def mock_login():
    return call_castlemock("POST", "xpABue/auth", {"username": "demo_user", "password": "secret"})


@app.put("/external/user/update", tags=["CastleMock"], summary="Mock user update via CastleMock")
def update_user_profile():
    return call_castlemock("PUT", "kCpnzj/user/update")
