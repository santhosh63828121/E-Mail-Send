import os

# Load environment variables from a .env fi

class Config:
    # Database configuration (Neon PostgreSQL)
    SQLALCHEMY_DATABASE_URI = "postgresql://AppointmentDoc_owner:npg_msJxbhi8jq9z@ep-young-shape-a8y2y3ci-pooler.eastus2.azure.neon.tech/AppointmentDoc?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "sksk20634@gmail.com"
    MAIL_PASSWORD = "zwuxrjylataldqfa"

    # CORS Settings
    CORS_HEADERS = "Content-Type"
