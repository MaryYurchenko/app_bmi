from fastapi import FastAPI
from app.database import init_db
from app.routers import users, profiles, records, bmi

app = FastAPI(title="BMI Tracker API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(records.router)
app.include_router(bmi.router)