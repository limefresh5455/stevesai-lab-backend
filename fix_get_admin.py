with open("app/api/v1/content.py", "r") as f:
    content = f.read()

bad_service = """@router.get("/admin/services/{identifier}", response_model=ServiceOut)
def get_admin_service(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("services").select("*").eq("id", id).execute()"""

good_service = """@router.get("/admin/services/{identifier}", response_model=ServiceOut)
def get_admin_service(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(identifier)
        res = db.table("services").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("services").select("*").eq("slug", identifier).execute()"""

bad_blog = """@router.get("/admin/blogs/{identifier}", response_model=BlogOut)
def get_admin_blog(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("blog_posts").select("*").eq("id", id).execute()"""

good_blog = """@router.get("/admin/blogs/{identifier}", response_model=BlogOut)
def get_admin_blog(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(identifier)
        res = db.table("blog_posts").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("blog_posts").select("*").eq("slug", identifier).execute()"""

content = content.replace(bad_service, good_service)
content = content.replace(bad_blog, good_blog)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
