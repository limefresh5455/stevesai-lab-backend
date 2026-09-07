from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

PAGE_ID = "d6ee81a8-bc4e-462e-8d29-54562828b20c"

# Fetch the existing page
response = client.get(f"/api/v1/admin/pages/{PAGE_ID}")
page = response.json()
print("Before content keys:", list(page["content"].keys())[:5])

# Update just a tiny part of the content JSON
payload = {
    "content": {
        "heroBgImage": "/images/new-bg.png"
    }
}
update_response = client.put(f"/api/v1/admin/pages/{PAGE_ID}", json=payload)
updated_page = update_response.json()
print("After content keys:", list(updated_page["content"].keys())[:5])
print("Hero image:", updated_page["content"].get("heroBgImage"))
