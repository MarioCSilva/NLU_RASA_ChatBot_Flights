from sqlalchemy.orm import Session
import sql_app.schemas.feedback as FeedbackSchemas
from sql_app import models
def create_feedback(db: Session, feedback_data: FeedbackSchemas.FeedBackCreate):
    db_feedback = models.Feedback(
        user_id=feedback_data.user_id,
        rating=feedback_data.rating
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    return FeedbackSchemas.FeedBack(**db_feedback.__dict__)