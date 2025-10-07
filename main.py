
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from bson import ObjectId
from pymongo import MongoClient, ASCENDING
from faker import Faker

app = FastAPI()
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

@app.post("/students/", response_model=StudentOut)
def create_student(student: Student):
    if students.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    result = students.insert_one(student.dict())
    return to_out(students.find_one({"_id": result.inserted_id}), StudentOut)

@app.get("/students/", response_model=List[StudentOut])
def list_students():
    return [to_out(doc, StudentOut) for doc in students.find()]

@app.post("/courses/", response_model=CourseOut)
def create_course(course: Course):
    result = courses.insert_one(course.dict())
    return to_out(courses.find_one({"_id": result.inserted_id}), CourseOut)

@app.get("/courses/", response_model=List[CourseOut])
def list_courses():
    return [to_out(doc, CourseOut) for doc in courses.find()]

@app.post("/enrollments/", response_model=EnrollmentOut)
def enroll(enrollment: Enrollment):
    if not students.find_one({"_id": ObjectId(enrollment.student_id)}):
        raise HTTPException(status_code=404, detail="Student not found")
    if not courses.find_one({"_id": ObjectId(enrollment.course_id)}):
        raise HTTPException(status_code=404, detail="Course not found")
    result = enrollments.insert_one({
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    })
    return to_out(enrollments.find_one({"_id": result.inserted_id}), EnrollmentOut)

@app.get("/enrollments/", response_model=List[EnrollmentOut])
def list_enrollments():
    return [to_out(doc, EnrollmentOut) for doc in enrollments.find()]

@app.post("/seed/")
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
