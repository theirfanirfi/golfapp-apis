from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from Config import Config
from flask_marshmallow import Marshmallow
app = Flask(__name__)

db = SQLAlchemy(app)
ma = Marshmallow(app)


bcrypt = Bcrypt()

app = Flask(__name__)
app.config.from_object(Config)

#filters
app.jinja_env.filters['str'] = str()

#initializations
db.app = app
db.init_app(app)
bcrypt.init_app(app)

from golfrica_app.Models.models import Country
from golfrica_app.Views.Countries.Countries import Countries
from golfrica_app.Views.Clubs.Clubs import Clubs
from golfrica_app.Views.Statuses.Sync import Sync
from golfrica_app.Views.Statuses.Statuses import Statuses
from golfrica_app.Views.Like import Like
from golfrica_app.Views.Statuses.Comment import Comment


migrate = Migrate(app, db)

Countries.register(app)
Clubs.register(app)
Sync.register(app)
Statuses.register(app)
Like.register(app)
Comment.register(app)

