from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

slug = "test-camel-case-slug"

# create
client.post("/api/v1/admin/case-studies", json={"slug": slug, "title": "Original"})

payload = {
    "title": "Camel Case Test",
    "heroImage": "https://new-image-url.com/image.png",
    "year": "2030"
}

response = client.put(f"/api/v1/admin/case-studies/{slug}", json=payload)
print(response.status_code)
if response.status_code == 200:
    data = response.json()
    print("hero_image:", data.get("hero_image"))
    print("project_year:", data.get("project_year"))
else:
    print(response.text)
    
client.delete(f"/api/v1/admin/case-studies/{slug}")
