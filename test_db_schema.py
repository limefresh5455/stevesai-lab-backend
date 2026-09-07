from app.database import get_db
db = next(get_db())

# Let's get a page
res = db.table("pages").select("*").limit(1).execute()
if res.data:
    print("Page:", res.data[0])
else:
    print("No pages found")
