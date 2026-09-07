from app.database import get_db
db = next(get_db())
try:
    res = db.storage.create_bucket("website-media")
    print("Bucket created:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
