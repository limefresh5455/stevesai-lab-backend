import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

footer_api = """
# --- FOOTER ---
@router.get("/footer")
def get_footer(db: Client = Depends(get_db)):
    res = db.table("pages").select("*").eq("slug", "footer").eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Footer not found")
    return res.data[0]
"""

if "/footer" not in content:
    content += "\n" + footer_api
    with open("app/api/v1/content.py", "w") as f:
        f.write(content)
    print("Footer API added")
else:
    print("Footer API already exists")
