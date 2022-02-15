from flask import Flask
from app_package_folder.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail #<---Here


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail() #<---Here

def create_app(config_class_test=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class_test)

    db.init_app(app)
    login_manager.init_app(app)

    mail.init_app(app) #<--- Here

    from app_package_folder.routes import users
    from app_package_folder.errors_handling import bp
    
    app.register_blueprint(users)
    app.register_blueprint(bp)
    
    return app