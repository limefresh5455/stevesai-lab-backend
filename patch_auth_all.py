import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

# Replace any admin function in content.py
content = re.sub(
    r'(def (list_admin_[a-zA-Z0-9_]+|get_admin_[a-zA-Z0-9_]+)\(.*?)(db:\s*Client\s*=\s*Depends\(get_db\))(\s*\):)',
    r'\1\3, admin: dict = Depends(get_admin_from_cookie)\4',
    content
)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)

with open("app/api/v1/media.py", "r") as f:
    media = f.read()

media = re.sub(
    r'(def list_media\(.*?)(db:\s*Client\s*=\s*Depends\(get_db\))(\s*\):)',
    r'\1\2, admin: dict = Depends(get_admin_from_cookie)\3',
    media
)
with open("app/api/v1/media.py", "w") as f:
    f.write(media)

with open("app/api/v1/contact.py", "r") as f:
    contact = f.read()

if "get_admin_from_cookie" not in contact:
    contact = contact.replace("from app.database import get_db", "from app.database import get_db\nfrom app.api.v1.auth import get_admin_from_cookie")

contact = re.sub(
    r'(def get_contacts\(.*?)(db:\s*Client\s*=\s*Depends\(get_db\))(\s*\):)',
    r'\1\2, admin: dict = Depends(get_admin_from_cookie)\3',
    contact
)

contact = re.sub(
    r'(def delete_contact\(.*?)(db:\s*Client\s*=\s*Depends\(get_db\))(\s*\):)',
    r'\1\2, admin: dict = Depends(get_admin_from_cookie)\3',
    contact
)

with open("app/api/v1/contact.py", "w") as f:
    f.write(contact)

