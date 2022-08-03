# src/main.py

from pathlib import Path

import uvicorn
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.datastructures import URL

import crud
import models
import schemas
from config import get_settings
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory=str(Path(Path(__file__).resolve().parent, "templates")))

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "static"),
    name="static",
)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    # message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        if not validators.between(len(url.target_url), min=1, max=250):
            raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return get_admin_info(db_url)


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        db_url.url = db_url.key
        db_url.admin_url = db_url.secret_key
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
