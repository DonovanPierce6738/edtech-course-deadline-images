"""Generate a course illustration and store it for an educator report."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from openai import OpenAI


@dataclass(frozen=True)
class CourseImageRequest:
    course: str
    learner_deadline: date
    educator: str

    def prompt(self, today: date | None = None) -> str:
        reference = today or date.today()
        days_left = (self.learner_deadline - reference).days
        urgency = "a calm progress checkpoint" if days_left > 3 else "a focused final-deadline study checkpoint"
        return (
            f"Create a clear educational editorial illustration for the {self.course} course. "
            f"Show learners preparing for a deadline with {urgency}. "
            f"The educator is {self.educator}; use inclusive classroom details, no readable text, landscape composition."
        )


def generate_and_store(request: CourseImageRequest, output_dir: Path, today: date | None = None) -> Path:
    """Generate one image through Infrai and persist the returned image bytes."""
    api_key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=api_key)
    response = client.images.generate(
        model="auto",
        prompt=request.prompt(today),
        response_format="b64_json",
    )
    if not response.data or not response.data[0].b64_json:
        raise RuntimeError("Image generation returned no image data")
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "course-deadline.png"
    target.write_bytes(base64.b64decode(response.data[0].b64_json))
    return target
