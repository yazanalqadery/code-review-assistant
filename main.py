from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
from ai_client import generate_review
from database import Base, engine, get_db
from schemas import SubmissionCreate, SubmissionOut, UserCreate, UserOut

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/submissions", response_model=SubmissionOut)
async def create_submission(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    db_submission = crud.create_submission(db, submission)
    try:
        feedback = await generate_review(db_submission.code, db_submission.language)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "Submission was saved, but AI review generation failed.",
                "submission_id": db_submission.id,
                "reason": str(e),
            },
        ) from e
    crud.create_review(db, db_submission.id, feedback)
    db.refresh(
        db_submission
    )  # Refresh the submission to include the newly created review
    return db_submission


@app.get("/api/submissions/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: int, db: Session = Depends(get_db)):  # noqa: B008
    submission = crud.get_submission(db, submission_id)

    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No submission found"},
        )
    return submission


@app.get("/api/submissions", response_model=list[SubmissionOut])
def list_submissions(db: Session = Depends(get_db)):  # noqa: B008
    return crud.list_submissions(db)


@app.post("/api/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    return crud.create_user(db, user)


@app.get("/api/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):  # noqa: B008
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No user found"}
        )
    return user


@app.post("/api/submissions/{submission_id}/review", response_model=SubmissionOut)
async def create_review_for_submission(
    submission_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    submission = crud.get_submission(db, submission_id)
    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No submission found"},
        )

    if submission.review is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "Review already exists for this submission"},
        )

    try:
        feedback = await generate_review(submission.code, submission.language)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "AI review generation failed.",
                "submission_id": submission.id,
                "reason": str(e),
            },
        ) from e
    crud.create_review(db, submission.id, feedback)
    db.refresh(submission)  # Refresh the submission to include the newly created review
    return submission
