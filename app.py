from flask_migrate import Migrate
from server import create_app, db
from server.services import pill_service
import os

app = create_app('prod')
migrate = Migrate(app, db)

app.app_context().push()

db.create_all()

if __name__ == '__main__':
  app.run()