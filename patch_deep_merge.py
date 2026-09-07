import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

merge_func = """
def deep_merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(destination.get(key), dict):
            deep_merge(value, destination[key])
        else:
            destination[key] = value
    return destination
"""

if "def deep_merge" not in content:
    content = content.replace("router = APIRouter()", "router = APIRouter()\n" + merge_func)

for table, var in [("blog_posts", "blog"), ("services", "service"), ("case_studies", "case_study"), ("pages", "page")]:
    old_block = f"""    data = {var}.model_dump(exclude_unset=True)
    if not data:
        return res.data[0]
    update_res = db.table("{table}").update(data).eq("id", id).execute()"""
    
    new_block = f"""    data = {var}.model_dump(exclude_unset=True)
    if not data:
        return res.data[0]
    
    # Deep merge incoming data into existing DB row to prevent overwriting nested JSON fields
    merged_data = deep_merge(data, res.data[0])
    
    update_res = db.table("{table}").update(merged_data).eq("id", id).execute()"""
    
    content = content.replace(old_block, new_block)

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
