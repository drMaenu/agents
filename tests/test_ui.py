from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_ui_endpoint_returns_html() -> None:
    response = client.get("/chat-ui")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]