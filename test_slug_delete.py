from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

slug = "the-chatbot-that-actually-knew-the-product-replacing-a-generic-bot-with-a-custom-llm"
response = client.delete(f"/api/v1/admin/case-studies/{slug}")
print(response.status_code)
print(response.json())
