from server import db
from server.models.Pill import Pill
from server.models.Enterprise import Enterprise

def create_pill(data):
    pill = Pill.query.filter_by(pill_id=data['pill_id']).first()
    if not pill:
        enterprise = Enterprise.query.filter_by(enterprise_id)

        new_enterprise = Enterprise(
                name = data['enterprise_name'],
                enterprise_id = data['enterprise_id']
        )

        new_pill = Pill(
            pill_id = data['pill_id'],
            name = data['name'],
            eng_name = data['eng_name'],
            chart = data['chart'],
            image_url = data['image_url'],
            class_name = data['class_name'],
            otc_type = data['otc_type'],
            enterprise = enterprise
        )

        db.session.add(enterprise)
        db.session.add(new_pill)
        db.session.commit()

    else:
        response_object = {
            'code': 'error',
            'message': 'Pill already exists.'
        }

        return response_object, 409

def get_all_pills():
    return Pill.query.all()
