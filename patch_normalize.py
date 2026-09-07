import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

normalize_func = """
import re
def normalize_keys(data):
    new_data = {}
    for k, v in data.items():
        if k == "year":
            new_data["project_year"] = v
            continue
        snake_k = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
        new_data[snake_k] = v
    return new_data
"""

if "def normalize_keys" not in content:
    content = content.replace("TABLE_COLUMNS = {", normalize_func + "\nTABLE_COLUMNS = {")

# For POST:
#     data = {var}.model_dump()
#     data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["{table}"]}
# Needs to become:
#     data = {var}.model_dump()
#     data = normalize_keys(data)
#     data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["{table}"]}

content = content.replace("data = blog.model_dump()\n    data = {k:", "data = blog.model_dump()\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = service.model_dump()\n    data = {k:", "data = service.model_dump()\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = case_study.model_dump()\n    data = {k:", "data = case_study.model_dump()\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = page.model_dump()\n    data = {k:", "data = page.model_dump()\n    data = normalize_keys(data)\n    data = {k:")

# For PUT:
#     data = {var}.model_dump(exclude_unset=True)
#     data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["{table}"]}

content = content.replace("data = blog.model_dump(exclude_unset=True)\n    data = {k:", "data = blog.model_dump(exclude_unset=True)\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = service.model_dump(exclude_unset=True)\n    data = {k:", "data = service.model_dump(exclude_unset=True)\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = case_study.model_dump(exclude_unset=True)\n    data = {k:", "data = case_study.model_dump(exclude_unset=True)\n    data = normalize_keys(data)\n    data = {k:")
content = content.replace("data = page.model_dump(exclude_unset=True)\n    data = {k:", "data = page.model_dump(exclude_unset=True)\n    data = normalize_keys(data)\n    data = {k:")

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
