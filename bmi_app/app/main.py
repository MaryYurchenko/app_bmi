from fastapi import FastAPI
from app.routers import users, profiles, records, bmi

app = FastAPI(title="BMI Tracker API")

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(records.router)
app.include_router(bmi.router)