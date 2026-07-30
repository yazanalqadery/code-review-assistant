from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
from database import Base, engine, get_db
from schemas import SubmissionCreate, SubmissionOut

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/submissions", response_model=SubmissionOut)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):  # noqa: B008
    return crud.create_submission(db, submission)


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
