from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from bson import ObjectId
from pymongo import MongoClient, ASCENDING
from faker import Faker

# 📋 Настраиваем порядок и описание секций (tags)
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
    openapi_tags=tags_metadata
)

fake = Faker()

client = MongoClient("mongodb://mongo:27017")
db = client["university_api"]

students = db["students"]
courses = db["courses"]
enrollments = db["enrollments"]

students.create_index([("email", ASCENDING)], unique=True)
courses.create_index([("title", ASCENDING)])
enrollments.create_index([("student_id", ASCENDING), ("course_id", ASCENDING)], unique=True)

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

def to_out(doc, model):
    return model(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})

@app.post("/students/", response_model=StudentOut, tags=["Students"])
def create_student(student: Student):
    if students.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    result = students.insert_one(student.dict())
    return to_out(students.find_one({"_id": result.inserted_id}), StudentOut)

@app.get("/students/", response_model=List[StudentOut], tags=["Students"])
def list_students():
    return [to_out(doc, StudentOut) for doc in students.find()]

@app.put("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def update_student(student_id: str, student: Student):
    result = students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = students.find_one({"_id": ObjectId(student_id)})
    return to_out(updated, StudentOut)

@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK, tags=["Students"])
def delete_student(student_id: str):
    result = students.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    enrollments.delete_many({"student_id": ObjectId(student_id)})
    return {"status": "deleted", "entity": "student", "id": student_id}

@app.post("/courses/", response_model=CourseOut, tags=["Courses"])
def create_course(course: Course):
    result = courses.insert_one(course.dict())
    return to_out(courses.find_one({"_id": result.inserted_id}), CourseOut)

@app.get("/courses/", response_model=List[CourseOut], tags=["Courses"])
def list_courses():
    return [to_out(doc, CourseOut) for doc in courses.find()]

@app.put("/courses/{course_id}", response_model=CourseOut, tags=["Courses"])
def update_course(course_id: str, course: Course):
    result = courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": course.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    updated = courses.find_one({"_id": ObjectId(course_id)})
    return to_out(updated, CourseOut)

@app.delete("/courses/{course_id}", status_code=status.HTTP_200_OK, tags=["Courses"])
def delete_course(course_id: str):
    result = courses.delete_one({"_id": ObjectId(course_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    enrollments.delete_many({"course_id": ObjectId(course_id)})
    return {"status": "deleted", "entity": "course", "id": course_id}

@app.post("/enrollments/", response_model=EnrollmentOut, tags=["Enrollments"])
def create_enrollment(enrollment: Enrollment):
    if not students.find_one({"_id": ObjectId(enrollment.student_id)}):
        raise HTTPException(status_code=404, detail="Student not found")
    if not courses.find_one({"_id": ObjectId(enrollment.course_id)}):
        raise HTTPException(status_code=404, detail="Course not found")
    result = enrollments.insert_one({
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    })
    return to_out(enrollments.find_one({"_id": result.inserted_id}), EnrollmentOut)

@app.get("/enrollments/", response_model=List[EnrollmentOut], tags=["Enrollments"])
def list_enrollments():
    return [to_out(doc, EnrollmentOut) for doc in enrollments.find()]

@app.put("/enrollments/{enrollment_id}", response_model=EnrollmentOut, tags=["Enrollments"])
def update_enrollment(enrollment_id: str, enrollment: Enrollment):
    # Проверяем, что студент и курс существуют
    if not students.find_one({"_id": ObjectId(enrollment.student_id)}):
        raise HTTPException(status_code=404, detail="Student not found")
    if not courses.find_one({"_id": ObjectId(enrollment.course_id)}):
        raise HTTPException(status_code=404, detail="Course not found")

    result = enrollments.update_one(
        {"_id": ObjectId(enrollment_id)},
        {"$set": enrollment.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    updated = enrollments.find_one({"_id": ObjectId(enrollment_id)})
    return to_out(updated, EnrollmentOut)

@app.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_200_OK, tags=["Enrollments"])
def delete_enrollment(enrollment_id: str):
    result = enrollments.delete_one({"_id": ObjectId(enrollment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"status": "deleted", "entity": "enrollment", "id": enrollment_id}

@app.post("/seed/", tags=["Utility"])
def seed_data():
    students.delete_many({})
    courses.delete_many({})
    enrollments.delete_many({})

    student_ids = [students.insert_one({
        "name": fake.name(),
        "age": fake.random_int(min=18, max=30),
        "email": fake.unique.email()
    }).inserted_id for _ in range(5)]

    course_ids = [courses.insert_one({
        "title": fake.job(),
        "description": fake.text(max_nb_chars=50)
    }).inserted_id for _ in range(3)]

    for sid in student_ids:
        enrollments.insert_one({
            "student_id": str(sid),
            "course_id": str(fake.random_element(course_ids))
        })

    return {"message": "Database seeded successfully"}

@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}

import requests

# ⚙️ Эндпоинт для обращения к CastleMock
@app.get("/external/weather", tags=["CastleMock"], summary="Get mock weather from CastleMock")
def get_mock_weather():
    try:
        url = "http://castlemock:8080/castlemock/mock/rest/project/KKWaVE/application/CwpPop/forecast"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"CastleMock error: {e}")
