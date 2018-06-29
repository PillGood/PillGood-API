from server import db

class Enterprise(db.Model):
    __tablename__ = 'enterprise'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    enterprise_id = db.Column(db.String(20), nullable=False, unique=True)

    pills = db.relationship('Pill', backref='enterprise', lazy=True)

