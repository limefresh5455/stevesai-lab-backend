import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

for table, var in [("blog_posts", "blog"), ("services", "service"), ("case_studies", "case_study"), ("pages", "page")]:
    old_block = f"""    data = {var}.model_dump(exclude_unset=True)
    update_res = db.table("{table}").update(data).eq("id", id).execute()
    return update_res.data[0]"""
    
    new_block = f"""    data = {var}.model_dump(exclude_unset=True)
    if not data:
        return res.data[0]
    update_res = db.table("{table}").update(data).eq("id", id).execute()
    if not update_res.data:
        return res.data[0]
    return update_res.data[0]"""
    
    content = content.replace(old_block, new_block)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
