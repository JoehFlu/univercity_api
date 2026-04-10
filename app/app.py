from fastapi import FastAPI

from app.config import APP_TITLE, APP_VERSION, TAGS_METADATA
from app.db import ensure_indexes
from app.routers import courses, enrollments, external, students, utility


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    openapi_tags=TAGS_METADATA,
)

app.include_router(utility.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(external.router)


@app.on_event("startup")
def startup_event():
    ensure_indexes()
