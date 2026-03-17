from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "items": items}
    )


@app.get("/create")
def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
def create_item(
    name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)
):

    crud.create_item(db, name, description)

    return RedirectResponse("/", status_code=303)


@app.get("/edit/{item_id}")
def edit_page(item_id: int, request: Request, db: Session = Depends(get_db)):

    item = crud.get_item(db, item_id)

    return templates.TemplateResponse("edit.html", {"request": request, "item": item})


@app.post("/edit/{item_id}")
def edit_item(
    item_id: int,
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
):

    crud.update_item(db, item_id, name, description)

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    crud.delete_item(db, item_id)

    return RedirectResponse("/", status_code=303)
