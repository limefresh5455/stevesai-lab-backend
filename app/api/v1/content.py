import uuid
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from typing import List
from app.database import get_db
from app.schemas.content import BlogOut, BlogCreate, BlogUpdate, ServiceOut, ServiceCreate, ServiceUpdate, CaseStudyOut, CaseStudyCreate, CaseStudyUpdate
from app.api.v1.auth import get_admin_from_cookie

router = APIRouter()


import re
def normalize_keys(data):
    new_data = {}
    for k, v in data.items():
        if k == "year":
            new_data["project_year"] = v
            continue
        snake_k = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
        new_data[snake_k] = v
    return new_data

TABLE_COLUMNS = {
    "blog_posts": ['id', 'slug', 'title', 'description', 'category', 'author', 'author_initial', 'published_date', 'read_time', 'hero_image', 'sections', 'faqs', 'status', 'created_at', 'updated_at'],
    "services": ['id', 'slug', 'title', 'label', 'description', 'hero_title', 'highlighted_title', 'hero_description', 'technologies', 'stats', 'features_section', 'approach', 'engagements_section', 'case_study', 'status', 'created_at', 'updated_at'],
    "case_studies": ['id', 'slug', 'title', 'category', 'industry', 'project_year', 'location', 'description', 'hero_image', 'highlights', 'sections', 'status', 'created_at', 'updated_at'],
    "pages": ['id', 'slug', 'title', 'content', 'status', 'published_at', 'created_at', 'updated_at']
}


def deep_merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(destination.get(key), dict):
            deep_merge(value, destination[key])
        else:
            destination[key] = value
    return destination


# --- BLOGS ---
@router.get("/blogs", response_model=List[BlogOut])
def list_blogs(db: Client = Depends(get_db)):
    res = db.table("blog_posts").select("*").eq("status", "published").execute()
    return res.data

@router.get("/blogs/{slug}", response_model=BlogOut)
def get_blog(slug: str, db: Client = Depends(get_db)):
    res = db.table("blog_posts").select("*").eq("slug", slug).eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return res.data[0]

@router.post("/admin/blogs", response_model=BlogOut)
def create_blog(blog: BlogCreate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    data = blog.model_dump()
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["blog_posts"]}
    res = db.table("blog_posts").insert(data).execute()
    return res.data[0]

@router.put("/admin/blogs/{id}", response_model=BlogOut)
def update_blog(id: str, blog: BlogUpdate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("blog_posts").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("blog_posts").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Blog not found")
    data = blog.model_dump(exclude_unset=True)
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["blog_posts"]}
    if not data:
        return res.data[0]
    
    # Deep merge incoming data into existing DB row to prevent overwriting nested JSON fields
    merged_data = deep_merge(data, res.data[0])
    
    update_res = db.table("blog_posts").update(merged_data).eq(query_key, id).execute()
    if not update_res.data:
        return res.data[0]
    return update_res.data[0]

@router.delete("/admin/blogs/{id}")
def delete_blog(id: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("blog_posts").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("blog_posts").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.table("blog_posts").delete().eq(query_key, id).execute()
    return {"message": "Blog deleted"}


# --- SERVICES ---
@router.get("/admin/services", response_model=List[ServiceOut])
def list_admin_services(db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("services").select("*").order("id").execute()
    return res.data

@router.get("/services", response_model=List[ServiceOut])
def list_services(db: Client = Depends(get_db)):
    res = db.table("services").select("*").eq("status", "published").order("id").execute()
    return res.data

@router.get("/services/{slug}", response_model=ServiceOut)
def get_service(slug: str, db: Client = Depends(get_db)):
    res = db.table("services").select("*").eq("slug", slug).eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Service not found")
    return res.data[0]

@router.post("/admin/services", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    data = service.model_dump()
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["services"]}
    res = db.table("services").insert(data).execute()
    return res.data[0]

@router.put("/admin/services/{id}", response_model=ServiceOut)
def update_service(id: str, service: ServiceUpdate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("services").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("services").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Service not found")
    data = service.model_dump(exclude_unset=True)
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["services"]}
    if not data:
        return res.data[0]
    
    # Deep merge incoming data into existing DB row to prevent overwriting nested JSON fields
    merged_data = deep_merge(data, res.data[0])
    
    update_res = db.table("services").update(merged_data).eq(query_key, id).execute()
    if not update_res.data:
        return res.data[0]
    return update_res.data[0]

@router.delete("/admin/services/{id}")
def delete_service(id: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("services").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("services").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Service not found")
    db.table("services").delete().eq(query_key, id).execute()
    return {"message": "Service deleted"}

# --- CASE STUDIES ---
@router.get("/admin/case-studies", response_model=List[CaseStudyOut])
def list_admin_case_studies(db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("case_studies").select("*").order("id").execute()
    return res.data

@router.get("/case-studies", response_model=List[CaseStudyOut])
def list_case_studies(db: Client = Depends(get_db)):
    res = db.table("case_studies").select("*").eq("status", "published").order("id").execute()
    return res.data

@router.get("/case-studies/{slug}", response_model=CaseStudyOut)
def get_case_study(slug: str, db: Client = Depends(get_db)):
    res = db.table("case_studies").select("*").eq("slug", slug).eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Case Study not found")
    return res.data[0]

@router.post("/admin/case-studies", response_model=CaseStudyOut)
def create_case_study(case_study: CaseStudyCreate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    data = case_study.model_dump()
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["case_studies"]}
    res = db.table("case_studies").insert(data).execute()
    return res.data[0]

@router.put("/admin/case-studies/{id}", response_model=CaseStudyOut)
def update_case_study(id: str, case_study: CaseStudyUpdate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("case_studies").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("case_studies").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Case Study not found")
    data = case_study.model_dump(exclude_unset=True)
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["case_studies"]}
    if not data:
        return res.data[0]
    
    # Deep merge incoming data into existing DB row to prevent overwriting nested JSON fields
    merged_data = deep_merge(data, res.data[0])
    
    update_res = db.table("case_studies").update(merged_data).eq(query_key, id).execute()
    if not update_res.data:
        return res.data[0]
    return update_res.data[0]

@router.delete("/admin/case-studies/{id}")
def delete_case_study(id: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("case_studies").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("case_studies").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Case Study not found")
    db.table("case_studies").delete().eq(query_key, id).execute()
    return {"message": "Case Study deleted"}

@router.get("/admin/case-studies/{identifier}", response_model=CaseStudyOut)
def get_admin_case_study(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(identifier)
        res = db.table("case_studies").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("case_studies").select("*").eq("slug", identifier).execute()
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Case Study not found")
    return res.data[0]

@router.get("/admin/services/{identifier}", response_model=ServiceOut)
def get_admin_service(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(identifier)
        res = db.table("services").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("services").select("*").eq("slug", identifier).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Service not found")
    return res.data[0]

@router.get("/admin/blogs/{identifier}", response_model=BlogOut)
def get_admin_blog(identifier: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(identifier)
        res = db.table("blog_posts").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("blog_posts").select("*").eq("slug", identifier).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return res.data[0]

@router.get("/admin/blogs", response_model=List[BlogOut])
def list_admin_blogs(db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("blog_posts").select("*").order("id", desc=True).execute()
    return res.data

# --- PAGES ---
from app.schemas.content import PageOut, PageCreate, PageUpdate

@router.get("/admin/pages", response_model=List[PageOut])
def list_admin_pages(db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("pages").select("*").order("id", desc=True).execute()
    return res.data

@router.get("/pages/{slug}", response_model=PageOut)
def get_page_public(slug: str, db: Client = Depends(get_db)):
    res = db.table("pages").select("*").eq("slug", slug).eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Page not found")
    return res.data[0]

@router.get("/admin/pages/{id}", response_model=PageOut)
def get_admin_page(id: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("pages").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("pages").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Page not found")
    return res.data[0]

@router.post("/admin/pages", response_model=PageOut)
def create_page(page: PageCreate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    data = page.model_dump()
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["pages"]}
    res = db.table("pages").insert(data).execute()
    return res.data[0]

@router.put("/admin/pages/{id}", response_model=PageOut)
def update_page(id: str, page: PageUpdate, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("pages").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("pages").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Page not found")
    data = page.model_dump(exclude_unset=True)
    data = normalize_keys(data)
    data = {k: v for k, v in data.items() if k in TABLE_COLUMNS["pages"]}
    if not data:
        return res.data[0]
    
    # Deep merge incoming data into existing DB row to prevent overwriting nested JSON fields
    merged_data = deep_merge(data, res.data[0])
    
    update_res = db.table("pages").update(merged_data).eq(query_key, id).execute()
    if not update_res.data:
        return res.data[0]
    return update_res.data[0]

@router.delete("/admin/pages/{id}")
def delete_page(id: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        uuid.UUID(id)
        res = db.table("pages").select("*").eq("id", id).execute()
        query_key = "id"
    except ValueError:
        res = db.table("pages").select("*").eq("slug", id).execute()
        query_key = "slug"
        
    if not res.data:
        raise HTTPException(status_code=404, detail="Page not found")
    db.table("pages").delete().eq(query_key, id).execute()
    return {"message": "Page deleted"}

@router.get("/admin/pages/slug/{slug}", response_model=PageOut)
def get_admin_page_by_slug(slug: str, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    res = db.table("pages").select("*").eq("slug", slug).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Page not found")
    return res.data[0]


# --- FOOTER ---
@router.get("/footer")
def get_footer(db: Client = Depends(get_db)):
    res = db.table("pages").select("*").eq("slug", "footer").eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Footer not found")
    return res.data[0]


# --- HEADER ---
@router.get("/header")
def get_header(db: Client = Depends(get_db)):
    res = db.table("pages").select("*").eq("slug", "header").eq("status", "published").execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Header not found")
    return res.data[0]
