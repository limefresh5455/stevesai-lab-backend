from app.database import get_db
db = next(get_db())

res = db.table("blog_posts").select("*").limit(1).execute()
first_blog = res.data[0]
print("Before:", {k: v for k, v in first_blog.items() if k in ["id", "title", "status"]})

update_res = db.table("blog_posts").update({"title": "Test Title Update"}).eq("id", first_blog["id"]).execute()
print("After update:", {k: v for k, v in update_res.data[0].items() if k in ["id", "title", "status"]})
