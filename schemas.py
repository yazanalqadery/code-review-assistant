from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SubmissionCreate(BaseModel):
    user_id: int
    code: str = Field(..., min_length=1, max_length=10000)
    language: str = Field(..., min_length=1, max_length=50)
    filename: str | None = Field(None, max_length=255)


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
    username: str = Field(..., min_length=1, max_length=50)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime
