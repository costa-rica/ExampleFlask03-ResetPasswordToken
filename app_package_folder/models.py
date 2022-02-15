from flask import current_app #<---HERE
from app_package_folder import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #<---HERE

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
    

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def get_reset_token(self, expires_sec=1800): #<---HERE
        s=Serializer(current_app.config['SECRET_KEY'], expires_sec) #<---HERE
        return s.dumps({'user_id': self.id}).decode('utf-8') #<---HERE

    @staticmethod#<-- HERE-This means self is not an argument the function should expect
    def verify_reset_token(token): #<---HERE
        s=Serializer(current_app.config['SECRET_KEY']) #<---HERE
        try: #<---HERE
            user_id = s.loads(token)['user_id'] #<---HERE
        except: #<---HERE
            return None #<---HERE
        return Users.query.get(user_id) #<---HERE

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.password}')"