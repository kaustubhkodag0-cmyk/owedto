from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database import engine, get_db, Base
from models import Commitment
from extractor import extract_commitments
import datetime
from scheduler import start_scheduler
load_dotenv()

Base.metadata.create_all(bind=engine)
start_scheduler()
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/upload")
def upload_transcript(
    request: Request,
    meeting_title: str = Form(...),
    transcript: str = Form(...),
    db: Session = Depends(get_db)
):
    commitments = extract_commitments(transcript)
    for c in commitments:
        deadline = None
        if c.get("deadline"):
            try:
                deadline = datetime.datetime.fromisoformat(c["deadline"])
            except:
                pass
        db_commitment = Commitment(
            meeting_title=meeting_title,
            owner=c["owner"],
            recipient=c["recipient"],
            deliverable=c["deliverable"],
            deadline=deadline
        )
        db.add(db_commitment)
    db.commit()
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    commitments = db.query(Commitment).order_by(
        Commitment.created_at.desc()
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"commitments": commitments, "now": datetime.datetime.utcnow()}
    )

@app.post("/complete/{commitment_id}")
def mark_complete(
    commitment_id: int,
    db: Session = Depends(get_db)
):
    c = db.query(Commitment).filter(
        Commitment.id == commitment_id
    ).first()
    if c:
        c.completed = True
        db.commit()
    return RedirectResponse("/dashboard", status_code=303)