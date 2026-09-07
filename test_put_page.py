from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)
client.app.dependency_overrides = app.dependency_overrides
from app.api.v1.auth import get_admin_from_cookie
client.app.dependency_overrides[get_admin_from_cookie] = lambda: {"id": 1}

payload = {
    "title": "test",
    "slug": "test",
    "content": {}
}

try:
    response = client.put("/api/v1/admin/pages/88a1faa1-d889-4720-b7b6-3f8544c155eb", json=payload)
    print(response.status_code)
    print(response.json())
except Exception as e:
    import traceback
    traceback.print_exc()
