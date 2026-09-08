import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

header_api = """
# --- HEADER ---
@router.get("/header")
def get_header(db: Client = Depends(get_db)):
    res = db.table("pages").select("*").eq("slug", "header").eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Header not found")
    return res.data[0]
"""

if "/header" not in content:
    content += "\n" + header_api
    with open("app/api/v1/content.py", "w") as f:
        f.write(content)
    print("Header API added")
else:
    print("Header API already exists")
