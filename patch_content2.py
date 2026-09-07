import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

content = re.sub(r'\s*data\["created_by"\] = admin\.get\("id"\)', '', content)
content = re.sub(r'\s*data\["updated_by"\] = admin\.get\("id"\)', '', content)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
