import sys

with open('backend/scripts/import_data.py', 'r') as f:
    code = f.read()

code = code.replace(
    '''        existing = db.query(Page).filter(Page.slug == slug).first()
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
            processed_page_slugs.add(slug)''',
    '''        existing = db.query(Page).filter(Page.slug == slug).first()
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
        processed_page_slugs.add(slug)'''
)

with open('backend/scripts/import_data.py', 'w') as f:
    f.write(code)
