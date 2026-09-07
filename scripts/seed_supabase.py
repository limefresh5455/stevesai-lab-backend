import sys
import os
import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from supabase import create_client
from app.core.config import settings


def get_exported_data_path() -> Path:
    return Path(__file__).resolve().parent.parent / "exported_data.json"


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_published_date(value):
    """
    Converts:
        August 12, 2026
    into:
        2026-08-12
    """

    if not value:
        return None

    try:
        return datetime.strptime(value, "%B %d, %Y").date().isoformat()
    except (TypeError, ValueError):
        print(f"Warning: Could not parse date: {value}")
        return None


def normalize_slug(item, item_type):
    slug = str(item.get("slug") or "").strip().strip("/")

    if not slug and item_type == "blog":
        href = str(item.get("href") or "").strip()
        slug = href.replace("/blog/", "").strip("/")

    return slug


def save_by_slug(db, table_name, slug, payload):
    """
    Insert the record when it does not exist.
    Update the record when its slug already exists.
    """

    existing = (
        db.table(table_name)
        .select("id")
        .eq("slug", slug)
        .limit(1)
        .execute()
    )

    if existing.data:
        payload["updated_at"] = current_timestamp()

        response = (
            db.table(table_name)
            .update(payload)
            .eq("slug", slug)
            .execute()
        )

        return "updated", response

    response = (
        db.table(table_name)
        .insert(payload)
        .execute()
    )

    return "inserted", response


def import_blogs(db, blogs):
    print(f"\nImporting {len(blogs)} blogs...")

    processed_slugs = set()

    for blog in blogs:
        slug = normalize_slug(blog, "blog")

        if not slug:
            print("Skipped blog without slug")
            continue

        if slug in processed_slugs:
            print(f"Skipped duplicate blog: {slug}")
            continue

        payload = {
            "slug": slug,
            "title": blog.get("title") or "Untitled",
            "description": (
                blog.get("description")
                or blog.get("excerpt")
            ),
            "category": blog.get("category"),
            "author": blog.get("author"),
            "author_initial": blog.get("author_initial"),
            "published_date": parse_published_date(blog.get("published_date")),
            "read_time": blog.get("read_time"),
            "hero_image": (
                blog.get("hero_image")
                or blog.get("image")
            ),
            "sections": blog.get("sections") or [],
            "faqs": blog.get("faqs") or [],
            "status": blog.get("status") or "published",
        }

        try:
            action, _ = save_by_slug(
                db,
                "blog_posts",
                slug,
                payload,
            )
            print(f"Blog {action}: {slug}")
        except Exception as error:
            print(f"Failed to import blog '{slug}': {error}")

        processed_slugs.add(slug)


def import_services(db, services):
    print(f"\nImporting {len(services)} services...")

    processed_slugs = set()

    for service in services:
        slug = normalize_slug(service, "service")

        if not slug:
            print("Skipped service without slug")
            continue

        if slug in processed_slugs:
            print(f"Skipped duplicate service: {slug}")
            continue

        payload = {
            "slug": slug,
            "title": service.get("title") or "Untitled",
            "label": service.get("label"),
            "description": service.get("description"),
            "hero_title": service.get("hero_title"),
            "highlighted_title": service.get("highlighted_title"),
            "hero_description": service.get("hero_description"),
            "technologies": service.get("technologies") or [],
            "stats": service.get("stats") or [],
            "features_section": service.get("features_section") or {},
            "approach": service.get("approach") or {},
            "engagements_section": (
                service.get("engagements_section") or {}
            ),
            "case_study": service.get("case_study") or {},
            "status": service.get("status") or "published",
        }

        try:
            action, _ = save_by_slug(
                db,
                "services",
                slug,
                payload,
            )
            print(f"Service {action}: {slug}")
        except Exception as error:
            print(f"Failed to import service '{slug}': {error}")

        processed_slugs.add(slug)


def import_case_studies(db, case_studies):
    print(f"\nImporting {len(case_studies)} case studies...")

    processed_slugs = set()

    for case_study in case_studies:
        slug = normalize_slug(case_study, "case-study")

        if not slug:
            print("Skipped case study without slug")
            continue

        if slug in processed_slugs:
            print(f"Skipped duplicate case study: {slug}")
            continue

        project_year = case_study.get("project_year")

        try:
            project_year = int(project_year) if project_year else None
        except (TypeError, ValueError):
            print(
                f"Warning: Invalid year for case study "
                f"'{slug}': {project_year}"
            )
            project_year = None

        payload = {
            "slug": slug,
            "title": case_study.get("title") or "Untitled",
            "category": case_study.get("category"),
            "industry": case_study.get("industry"),
            "project_year": project_year,
            "location": case_study.get("location"),
            "description": case_study.get("description"),
            "hero_image": case_study.get("hero_image"),
            "highlights": case_study.get("highlights") or [],
            "sections": case_study.get("sections") or [],
            "status": case_study.get("status") or "published",
        }

        try:
            action, _ = save_by_slug(
                db,
                "case_studies",
                slug,
                payload,
            )
            print(f"Case study {action}: {slug}")
        except Exception as error:
            print(f"Failed to import case study '{slug}': {error}")

        processed_slugs.add(slug)


def import_pages(db, pages):
    """
    Requires a pages table containing:
    slug, title, content, status, created_at and updated_at.
    """

    print(f"\nImporting {len(pages)} pages...")

    processed_slugs = set()

    for page in pages:
        slug = normalize_slug(page, "page")

        if not slug:
            print("Skipped page without slug")
            continue

        if slug in processed_slugs:
            print(f"Skipped duplicate page: {slug}")
            continue

        payload = {
            "slug": slug,
            "title": page.get("title") or "Untitled",
            "content": page.get("content") or {},
            "status": page.get("status") or "published",
        }

        try:
            action, _ = save_by_slug(
                db,
                "pages",
                slug,
                payload,
            )
            print(f"Page {action}: {slug}")
        except Exception as error:
            print(f"Failed to import page '{slug}': {error}")

        processed_slugs.add(slug)


def import_data():
    load_dotenv()

    url = (
        os.environ.get("SUPABASE_URL")
        or getattr(settings, "SUPABASE_URL", None)
    )

    key = (
        os.environ.get("SUPABASE_KEY")
        or getattr(settings, "SUPABASE_KEY", None)
    )

    if not url or not key:
        print("Missing SUPABASE_URL or SUPABASE_KEY")
        sys.exit(1)

    try:
        db = create_client(url, key)
    except Exception as error:
        print(f"Failed to create Supabase client: {error}")
        sys.exit(1)

    data_file = get_exported_data_path()

    if not data_file.exists():
        print(f"Exported data file not found: {data_file}")
        sys.exit(1)

    try:
        with data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {data_file}: {error}")
        sys.exit(1)
    except OSError as error:
        print(f"Could not read {data_file}: {error}")
        sys.exit(1)

    if not isinstance(data, dict):
        print("exported_data.json must contain a JSON object")
        sys.exit(1)

    import_blogs(db, data.get("blogs") or [])
    import_services(db, data.get("services") or [])
    import_case_studies(db, data.get("caseStudies") or [])
    import_pages(db, data.get("pages") or [])

    print("\nImport complete!")


if __name__ == "__main__":
    import_data()