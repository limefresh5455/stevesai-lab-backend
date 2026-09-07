import sys
with open('backend/scripts/import_data.py', 'r') as f:
    code = f.read()

# Make sure we import Page
if 'from app.models.content import Blog, Service, CaseStudy, Page' not in code:
    code = code.replace(
        'from app.models.content import Blog, Service, CaseStudy',
        'from app.models.content import Blog, Service, CaseStudy, Page'
    )

new_import_block = """
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
            processed_page_slugs.add(slug)
            
    db.commit()
"""
if "processed_page_slugs" not in code:
    code = code.replace('db.commit()', new_import_block)

with open('backend/scripts/import_data.py', 'w') as f:
    f.write(code)
