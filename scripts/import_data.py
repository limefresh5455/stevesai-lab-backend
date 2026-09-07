import sys
import os
import json
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.content import Blog, Service, CaseStudy, Page
from app.models.admin import Admin
from app.core.config import settings


def get_exported_data_path():
    return Path(__file__).resolve().parent.parent / "exported_data.json"


def import_data():
    db = SessionLocal()

    admin = db.query(Admin).filter(Admin.email == settings.ADMIN_EMAIL).first()
    admin_id = admin.id if admin else None

    data_file = get_exported_data_path()
    if not data_file.exists():
        raise FileNotFoundError(f"Export data file not found: {data_file}")

    with data_file.open("r") as f:
        data = json.load(f)

    print(f"Importing {len(data.get('blogs', []))} blogs...")
    processed_blog_slugs = set()
    for b in data.get("blogs", []):
        slug = b.get("href", "").replace("/blog/", "")
        if not slug:
            slug = b.get("slug", "")
            
        if slug in processed_blog_slugs:
            continue
            
        existing = db.query(Blog).filter(Blog.slug == slug).first()
        if not existing:
            content_json = json.dumps(b)
            
            new_blog = Blog(
                title=b.get("title", "Untitled"),
                slug=slug,
                excerpt=b.get("excerpt", ""),
                content=content_json,
                featured_image=b.get("image", ""),
                category=b.get("category", "General"),
                status="published",
                published_at=datetime.utcnow(),
                created_by=admin_id
            )
            db.add(new_blog)
            processed_blog_slugs.add(slug)
    
    print(f"Importing {len(data.get('services', []))} services...")
    processed_service_slugs = set()
    for s in data.get("services", []):
        slug = s.get("slug", "")
        if slug in processed_service_slugs:
            continue
            
        existing = db.query(Service).filter(Service.slug == slug).first()
        if not existing:
            new_service = Service(
                title=s.get("title", "Untitled"),
                slug=slug,
                short_description=s.get("description", ""),
                status="published",
                published_at=datetime.utcnow(),
                created_by=admin_id,
                hero_content=s.get("hero"),
                features=s.get("features"),
                process_steps=s.get("process"),
                faqs=s.get("faq"),
                related_case_studies=s.get("relatedCaseStudies")
            )
            db.add(new_service)
            processed_service_slugs.add(slug)
            
    print(f"Importing {len(data.get('caseStudies', []))} case studies...")
    processed_cs_slugs = set()
    for c in data.get("caseStudies", []):
        slug = c.get("slug", "")
        if slug in processed_cs_slugs:
            continue
            
        existing = db.query(CaseStudy).filter(CaseStudy.slug == slug).first()
        if not existing:
            new_cs = CaseStudy(
                title=c.get("title", "Untitled"),
                slug=slug,
                client=c.get("client", ""),
                industry=c.get("industry", ""),
                overview=c.get("overview", ""),
                challenge=c.get("challenge", ""),
                solution=c.get("solution", ""),
                status="published",
                published_at=datetime.utcnow(),
                created_by=admin_id,
                metrics=c.get("metrics"),
                process=c.get("process"),
                images=c.get("images")
            )
            db.add(new_cs)
            processed_cs_slugs.add(slug)
            
    
    print(f"Importing {len(data.get('pages', []))} pages...")
    processed_page_slugs = set()
    for p in data.get("pages", []):
        slug = p.get("slug", "")
        if not slug or slug in processed_page_slugs:
            continue
            
        existing = db.query(Page).filter(Page.slug == slug).first()
        if not existing:
            new_page = Page(
                title=p.get("title", "Untitled"),
                slug=slug,
                content=p.get("content", {}),
                status="published",
                published_at=datetime.utcnow(),
                created_by=admin_id
            )
            db.add(new_page)
        else:
            existing.title = p.get("title", existing.title)
            existing.content = p.get("content", existing.content)
            existing.status = "published"
            existing.updated_at = datetime.utcnow()
        processed_page_slugs.add(slug)
            
    db.commit()

    print("Import complete!")
    db.close()

if __name__ == "__main__":
    import_data()
