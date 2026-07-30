from sqlalchemy.orm import Session

from models import Review, Submission
from schemas import SubmissionCreate


def create_submission(db: Session, submission: SubmissionCreate) -> Submission:
    db_submission = Submission(
        user_id=submission.user_id,
        code=submission.code,
        language=submission.language,
        filename=submission.filename,
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_submission(db: Session, submission_id: int) -> Submission | None:
    return db.get(Submission, submission_id)


def list_submissions(db: Session) -> list[Submission]:
    return db.query(Submission).all()


def create_review(db: Session, submission_id: int, feedback: str) -> Review:
    db_review = Review(submission_id=submission_id, feedback=feedback)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
