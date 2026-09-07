import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

filter_code = """
TABLE_COLUMNS = {
    "blog_posts": ['id', 'slug', 'title', 'description', 'category', 'author', 'author_initial', 'published_date', 'read_time', 'hero_image', 'sections', 'faqs', 'status', 'created_at', 'updated_at'],
    "services": ['id', 'slug', 'title', 'label', 'description', 'hero_title', 'highlighted_title', 'hero_description', 'technologies', 'stats', 'features_section', 'approach', 'engagements_section', 'case_study', 'status', 'created_at', 'updated_at'],
    "case_studies": ['id', 'slug', 'title', 'category', 'industry', 'project_year', 'location', 'description', 'hero_image', 'highlights', 'sections', 'status', 'created_at', 'updated_at'],
    "pages": ['id', 'slug', 'title', 'content', 'status', 'published_at', 'created_at', 'updated_at']
}
"""

if "TABLE_COLUMNS = {" not in content:
    content = content.replace("router = APIRouter()", "router = APIRouter()\n" + filter_code)

for table, var in [("blog_posts", "blog"), ("services", "service"), ("case_studies", "case_study"), ("pages", "page")]:
    # Patch POST
    old_post = f"""    data = {var}.model_dump()
    res = db.table("{table}").insert(data).execute()"""
    new_post = f"""    data = {var}.model_dump()
    data = {{k: v for k, v in data.items() if k in TABLE_COLUMNS["{table}"]}}
    res = db.table("{table}").insert(data).execute()"""
    content = content.replace(old_post, new_post)
    
    # Patch PUT
    old_put = f"""    data = {var}.model_dump(exclude_unset=True)
    if not data:
        return res.data[0]"""
    new_put = f"""    data = {var}.model_dump(exclude_unset=True)
    data = {{k: v for k, v in data.items() if k in TABLE_COLUMNS["{table}"]}}
    if not data:
        return res.data[0]"""
    content = content.replace(old_put, new_put)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
