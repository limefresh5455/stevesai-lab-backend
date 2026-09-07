import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

# Add import uuid if not there
if "import uuid" not in content:
    content = "import uuid\n" + content

for table, var, title in [("blog_posts", "blog", "Blog"), ("services", "service", "Service"), ("case_studies", "case_study", "Case Study"), ("pages", "page", "Page")]:
    
    # Patch PUT
    old_put_select = f"""    res = db.table("{table}").select("*").eq("id", id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="{title} not found")"""
        
    new_put_select = f"""    try:
        uuid.UUID(id)
        res = db.table("{table}").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("{table}").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="{title} not found")"""

    content = content.replace(old_put_select, new_put_select)
    
    # We also need to update the update statement for PUT
    old_put_update = f"""    update_res = db.table("{table}").update(merged_data).eq("id", id).execute()"""
    new_put_update = f"""    update_res = db.table("{table}").update(merged_data).eq(query_key, id).execute()"""
    
    content = content.replace(old_put_update, new_put_update)

    # Patch DELETE
    old_delete_select = f"""    res = db.table("{table}").select("*").eq("id", id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="{title} not found")
    db.table("{table}").delete().eq("id", id).execute()"""
    
    new_delete_select = f"""    try:
        uuid.UUID(id)
        res = db.table("{table}").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("{table}").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="{title} not found")
    db.table("{table}").delete().eq(query_key, id).execute()"""

    content = content.replace(old_delete_select, new_delete_select)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
