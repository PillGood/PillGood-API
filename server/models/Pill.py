from server import db

class Pill(db.Model):
    __tablename__ = 'pill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pill_id = db.Column(db.String(20), nullable=False, unique=True)

    name = db.Column(db.String(200), nullable=False)
    eng_name = db.Column(db.String(200), nullable=False)
    
    chart = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    class_name = db.Column(db.String(20), nullable=False)
    otc_type = db.Column(db.String(20), nullable=False)

    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)