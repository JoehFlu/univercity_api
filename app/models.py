from pydantic import BaseModel, EmailStr


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
