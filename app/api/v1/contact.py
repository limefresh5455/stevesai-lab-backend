from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from supabase import Client
from app.database import get_db
from app.api.v1.auth import get_admin_from_cookie
from app.schemas.contact import ContactSubmissionCreate
from app.core.config import settings
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone

router = APIRouter()

def send_contact_email(name: str, email: str, message: str):
    if not settings.SMTP_HOST:
        print("SMTP_HOST not set, skipping email sending.")
        return

    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
    msg['Subject'] = f"New Contact Submission from {name}"
    msg['From'] = settings.SMTP_USER if settings.SMTP_USER else settings.CONTACT_EMAIL_TO
    msg['To'] = settings.CONTACT_EMAIL_TO

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

@router.post("/contact")
def submit_contact(
    submission: ContactSubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Client = Depends(get_db)
):
    try:
        data = {
            "name": submission.name,
            "email": submission.email,
            "message": submission.message,
            "status": "new",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Save to Supabase
        response = db.table("contact_submissions").insert(data).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to save submission")
            
        # Send email in background
        background_tasks.add_task(
            send_contact_email, 
            submission.name, 
            submission.email, 
            submission.message
        )
        
        return {"message": "Contact submission successful", "data": response.data[0]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contact")
def get_contacts(db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        response = db.table("contact_submissions").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/admin/contact-submissions/{submission_id}")
def delete_contact(submission_id: int, db: Client = Depends(get_db), admin: dict = Depends(get_admin_from_cookie)):
    try:
        response = db.table("contact_submissions").delete().eq("id", submission_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Submission not found")
        return {"message": "Submission deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
