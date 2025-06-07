from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.database.database import engine, Base
from app.config import settings

# Import modularized routers for admin, doctor, and patient
from app.modules.admin.routes import routers as admin_routers
from app.modules.doctor.routes import routers as doctor_routers
from app.modules.patient.routes import routers as patient_routers
from app.modules.user import user_router

# Initialize FastAPI app
app = FastAPI(title="IHMP API", version="1.0")

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# CORS configuration
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Trusted hosts (for production, specify your domain)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Register role-based routers
for router in admin_routers:
    app.include_router(router, prefix="/admin")
for router in doctor_routers:
    app.include_router(router, prefix="/doctor")
for router in patient_routers:
    app.include_router(router, prefix="/patient")

# Register user router (public endpoints)
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to the IHMP API"}