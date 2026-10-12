from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from src.edtech_images import CourseImageRequest, generate_and_store


def test_deadline_changes_the_learning_focus():
    request = CourseImageRequest("Physics lab", date(2026, 9, 15), "Ari")
    calm = request.prompt(date(2026, 9, 1))
    final = request.prompt(date(2026, 9, 13))
    assert "calm progress checkpoint" in calm
    assert "focused final-deadline study checkpoint" in final
    assert (request.learner_deadline - date(2026, 9, 13)).days == 2


def test_generate_requests_base64_image(tmp_path, monkeypatch):
    monkeypatch.setenv("INFRAI_API_KEY", "test-key")
    request = CourseImageRequest("Physics lab", date(2026, 9, 15), "Ari")
    with patch("src.edtech_images.OpenAI") as client:
        client.return_value.images.generate.return_value = SimpleNamespace(
            data=[SimpleNamespace(b64_json="cG5n")]
        )
        target = generate_and_store(request, tmp_path, date(2026, 9, 1))

    client.return_value.images.generate.assert_called_once_with(
        model="auto", prompt=request.prompt(date(2026, 9, 1)), response_format="b64_json"
    )
    assert target.read_bytes() == b"png"
