from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubmissionCreate(BaseModel):
    user_id: int
    code: str
    language: str
    filename: str | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    feedback: str
    created_at: datetime


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    code: str
    language: str
    filename: str | None
    created_at: datetime
    review: ReviewOut | None


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime
