from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())

    # mirrors Submission.user, one user has many submissions
    submissions = relationship("Submission", back_populates="user")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    code = Column(Text)
    language = Column(String)
    filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="submissions")
    # mirrors Review.submission, one submission has one review
    review = relationship("Review", back_populates="submission", uselist=False)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    # unique=True enforces the one-to-one at the DB level
    submission_id = Column(Integer, ForeignKey("submissions.id"), unique=True)
    feedback = Column(Text)
    created_at = Column(DateTime, default=func.now())

    submission = relationship("Submission", back_populates="review")
