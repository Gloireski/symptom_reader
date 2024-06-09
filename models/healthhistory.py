import uuid

from extensions import db


class HealthHistory(db.Model):
    __tablename__ = 'healthHistory'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    # def __init__(self):
    #     self.id = str(uuid.uuid4())
    def __repr__(self):
        return "<History '{}'>".format(self.date.strftime('%Y-%m-%d')+" "+self.diagnosis)
