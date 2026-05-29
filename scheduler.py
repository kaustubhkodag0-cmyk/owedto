import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from models import Commitment
from slack_bot import send_reminder
from dotenv import load_dotenv

load_dotenv()

scheduler = BackgroundScheduler()

def send_daily_reminders():
    print(f"Running daily reminders at {datetime.datetime.utcnow()}")
    db = SessionLocal()
    try:
        tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        due_soon = db.query(Commitment).filter(
            Commitment.completed == False,
            Commitment.reminded == False,
            Commitment.deadline <= tomorrow,
            Commitment.slack_owner_id != None
        ).all()
        print(f"Found {len(due_soon)} commitments to remind")
        for c in due_soon:
            success = send_reminder(
                slack_user_id=c.slack_owner_id,
                owner=c.owner,
                deliverable=c.deliverable,
                recipient=c.recipient,
                deadline=c.deadline
            )
            if success:
                c.reminded = True
                print(f"Reminded {c.owner} about: {c.deliverable}")
        db.commit()
    except Exception as e:
        print(f"Scheduler error: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(
        send_daily_reminders,
        'cron',
        hour=9,
        minute=0
    )
    scheduler.start()
    print("Scheduler started — reminders will fire daily at 9am UTC")