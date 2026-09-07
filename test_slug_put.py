from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

slug = "the-chatbot-that-actually-knew-the-product-replacing-a-generic-bot-with-a-custom-llm"
payload = {
    "title": "Updated Title via Slug"
}

# First check if this slug exists
res = client.get(f"/api/v1/case-studies/{slug}")
if res.status_code == 404:
    print("Slug not found. Creating a dummy one for test...")
    create_res = client.post("/api/v1/admin/case-studies", json={"slug": slug, "title": "Dummy"})
    print("Created:", create_res.status_code)

response = client.put(f"/api/v1/admin/case-studies/{slug}", json=payload)
print(response.status_code)
if response.status_code == 200:
    print(response.json()["title"])
else:
    print(response.text)
