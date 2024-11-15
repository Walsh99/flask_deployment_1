from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, nullable=False)
    module_code = db.Column(db.String(20), index=True, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, index=True)