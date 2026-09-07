from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

# Fetch the existing blog first
response = client.get("/api/v1/admin/blogs/6f4bd97d-b850-47d8-8e7f-6a7cd075fa4f")
blog = response.json()
print("Before:", blog["title"], blog["status"])

# Try to update ONLY the title
update_response = client.put("/api/v1/admin/blogs/6f4bd97d-b850-47d8-8e7f-6a7cd075fa4f", json={"title": "Updated Title via API"})
updated_blog = update_response.json()
print("After update:", updated_blog["title"], updated_blog["status"])
