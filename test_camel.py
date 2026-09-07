import re

def normalize_keys(data):
    new_data = {}
    for k, v in data.items():
        # Specific overrides
        if k == "year":
            new_data["project_year"] = v
            continue
        
        # camelCase to snake_case
        snake_k = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
        new_data[snake_k] = v
    return new_data

payload = {
    "title": "Test",
    "heroImage": "url",
    "authorInitial": "s",
    "readTime": 5,
    "year": "2025",
    "clientType": "B2B",
    "status": "draft"
}

print(normalize_keys(payload))
