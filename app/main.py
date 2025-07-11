from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.api import routes

app = FastAPI(
    title="YouthFit Pro API",
    description="Backend for Youth Fitness and Development Website",
    version="1.0.0"
)

# This points to the folder where main.py lives
BASE_DIR = Path(__file__).resolve().parent

# Serve static files from ./static relative to main.py
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Templates also relative to main.py
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(routes.router)
