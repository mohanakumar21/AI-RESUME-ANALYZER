from database import db
from flask_login import UserMixin
from datetime import datetime



class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    joined_date = db.Column(
    db.DateTime,
    default=datetime.utcnow
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


class ResumeHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    resume_name = db.Column(db.String(200))
    filename = db.Column(
        db.String(200)
    )

    ats_score = db.Column(
        db.Integer
    )

    match_score = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime
    )

    pdf_path = db.Column(
        db.String(300)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )