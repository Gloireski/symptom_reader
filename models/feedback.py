from app import db
import uuid


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

    def __init__(self):
        self.id = str(uuid.uuid4())
