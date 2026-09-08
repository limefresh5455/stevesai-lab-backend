from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Steve's AI Lab CMS"
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "website-media"
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_INITIAL_PASSWORD: str = "password"
    JWT_SECRET_KEY: str = "secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    FRONTEND_URL: str = "https://stevesai-lab.vercel.app",
    CORS_ALLOWED_ORIGINS: str = "https://stevesai-lab.vercel.app",
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    CONTACT_EMAIL_TO: str = "admin@example.com"
    class Config:
        env_file = ".env"

settings = Settings()
