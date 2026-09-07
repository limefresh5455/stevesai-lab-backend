import re

files = ["app/api/v1/content.py", "app/api/v1/media.py"]

for file_path in files:
    with open(file_path, "r") as f:
        content = f.read()
    
    # We want to match:
    # def func_name(..., admin: dict = Depends(get_admin_from_cookie)):
    # BUT only if it is immediately preceded by @router.get(...)
    
    # Split by @router.get
    parts = content.split("@router.get")
    new_content = parts[0]
    
    for part in parts[1:]:
        # Find the end of the def signature
        # Part looks like: '("/...", ...)\ndef func_name(..., admin: dict = Depends(get_admin_from_cookie)):\n...'
        
        # We can just replace ', admin: dict = Depends(get_admin_from_cookie)' with '' 
        # up until the first colon that closes the def
        
        def_match = re.search(r'def [^\(]+\((.*?)\):', part, re.DOTALL)
        if def_match:
            signature = def_match.group(1)
            new_signature = signature.replace(', admin: dict = Depends(get_admin_from_cookie)', '')
            part = part.replace(signature, new_signature, 1)
        
        new_content += "@router.get" + part
        
    with open(file_path, "w") as f:
        f.write(new_content)
