from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.routes.analyze import router
from app.core.templates import templates
from app.utils.context import get_base_context
from app.routes.devices import router as device_router
from app.database import create_db

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.include_router(router)
app.include_router(device_router)
create_db()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/")
def home(request: Request):
    context = get_base_context()
    context["result"] = "No analysis yet"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )

@app.get("/about")
def about():
    return {
        "developer": "Mohamed",
        "project": "Network Troubleshooter",
    }

@app.get("/health")
def health():
    return {"status": "OK"}
