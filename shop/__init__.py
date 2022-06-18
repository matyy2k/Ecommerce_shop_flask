from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

from flask_login import LoginManager
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'erttrrehtsrgt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Zaloguj się najpierw"

from .admin.models import Admin
from .customers.models import Customer

record = 0


@login_manager.user_loader
def load_user(user_id):
    global record
    if 'user_type' in session:
        if session["user_type"] == "admin":
            record = Admin.query.get(int(user_id))
        if session["user_type"] == "customer":
            record = Customer.query.get(int(user_id))
        return record


from shop.products import routes
from shop.admin import routes
from shop.carts import carts
from shop.customers import routes
# from shop.moderator import routes