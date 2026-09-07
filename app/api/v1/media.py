from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from supabase import Client
import uuid
import mimetypes
from datetime import datetime
from app.database import get_db
from app.api.v1.auth import get_admin_from_cookie
from app.core.config import settings

router = APIRouter()

@router.post("/admin/media/upload")
async def upload_file(
    file: UploadFile = File(...), 
    db: Client = Depends(get_db), 
    admin: dict = Depends(get_admin_from_cookie)
):
    try:
        # Read file content
        file_bytes = await file.read()
        
        # Generate a unique filename
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}" if file_ext else uuid.uuid4().hex
        
        # Upload to Supabase Storage
        content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        
        # Storage upload
        res = db.storage.from_(settings.SUPABASE_BUCKET).upload(
            file=file_bytes,
            path=unique_filename,
            file_options={"content-type": content_type}
        )
        
        # Get public URL
        public_url = db.storage.from_(settings.SUPABASE_BUCKET).get_public_url(unique_filename)
        
        # Insert record into media table
        media_data = {
            "filename": file.filename,
            "file_path": public_url,
            "mime_type": content_type,
            "size": len(file_bytes),
            "uploaded_by": admin.get("id"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        media_res = db.table("media").insert(media_data).execute()
        
        return {
            "message": "File uploaded successfully",
            "url": public_url,
            "media": media_res.data[0] if media_res.data else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/media")
def list_media(db: Client = Depends(get_db)):
    res = db.table("media").select("*").order("created_at", desc=True).execute()
    return res.data
