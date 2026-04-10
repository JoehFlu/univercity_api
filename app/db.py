from pymongo import ASCENDING, MongoClient

from app.config import MONGO_DB_NAME, MONGO_URL


client = MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB_NAME]

students = db["students"]
courses = db["courses"]
enrollments = db["enrollments"]


def ensure_indexes():
    students.create_index([("email", ASCENDING)], unique=True)
    courses.create_index([("title", ASCENDING)])
    enrollments.create_index(
        [("student_id", ASCENDING), ("course_id", ASCENDING)],
        unique=True,
    )
