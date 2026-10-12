from datetime import date, timedelta
from pathlib import Path

from src.edtech_images import CourseImageRequest, generate_and_store


request = CourseImageRequest(
    course="Intro to data literacy",
    learner_deadline=date.today() + timedelta(days=5),
    educator="Mina, the course facilitator",
)
path = generate_and_store(request, Path("generated"))
print(f"Stored {path} for {request.educator}'s {request.course} report")

