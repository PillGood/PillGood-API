from flask_migrate import Migrate
from server import create_app, db
from server.services import pill_service
import os

app = create_app(os.getenv('ENV') or 'dev')
migrate = Migrate(app, db)

app.app_context().push()

pill_service.create_pill({
  'pill_id': 12345,
  'name': '약 이름이다',
  'eng_name': 'yak irum',
  'chart': '이건 약이다',
  'image_url': 'http://google.com',
  'class_name': '마약',
  'otc_type': '마약류',
  'enterprise_name': '(주)약쟁이들',
  'enterprise_id': '12345'
})

if __name__ == '__main__':
  app.run()