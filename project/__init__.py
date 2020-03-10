from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_talisman import Talisman
from .config import DevelopmentConfig


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'info'
mail = Mail()
talisman = Talisman()

csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'cdn.jsdelivr.net'
    ],
    'script-src': ['\'self\'', 'use.fontawesome.com']
}

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    talisman.init_app(
        app, content_security_policy=csp, content_security_policy_nonce_in=['script-src']
    )
    
    from .users.routes import users
    from .expenses.routes import expenses
    app.register_blueprint(users)
    app.register_blueprint(expenses)

    return app
