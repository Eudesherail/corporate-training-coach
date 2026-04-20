from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import ProgressRecord, User


def seed_demo_data() -> None:
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@coach.com").first()
        employee = db.query(User).filter(User.email == "employee@coach.com").first()

        if not admin:
            admin = User(
                full_name="Avery Admin",
                email="admin@coach.com",
                password_hash=hash_password("Admin123!"),
                role="admin",
            )
            db.add(admin)

        if not employee:
            employee = User(
                full_name="Elliot Employee",
                email="employee@coach.com",
                password_hash=hash_password("Employee123!"),
                role="employee",
            )
            db.add(employee)

        db.commit()

        employee = db.query(User).filter(User.email == "employee@coach.com").first()
        if employee and not db.query(ProgressRecord).filter(ProgressRecord.user_id == employee.id).first():
            db.add(
                ProgressRecord(
                    user_id=employee.id,
                    module_name="New Hire Onboarding",
                    status="in_progress",
                    completion_percent=25,
                    notes="Welcome tasks assigned",
                )
            )
            db.commit()
    finally:
        db.close()
