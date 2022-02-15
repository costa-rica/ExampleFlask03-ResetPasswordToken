from flask import Blueprint, current_app
from flask import render_template, request, abort, render_template_string, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app_package_folder import db, mail #<---HERE
from app_package_folder.models import Users
import sqlalchemy
from flask_mail import Message #<---HERE

users = Blueprint('users', __name__)

@users.route("/",methods=["GET","POST"])
def home():
    if 'users' in sqlalchemy.inspect(db.engine).get_table_names():
        print('db already exists')
    else:
        db.create_all()
        print('db created')
    if request.method == 'POST':
        print('posted')
        return redirect(url_for('users.forgot')) #<---HERE
    return render_template_string("""
<h1>Home Page</h1><br/>
<form method="POST" action="" enctype="multipart/form-data">
<input type="submit" value="Forgot Password" />
</form>
""")

def send_reset_email(user): #<---HERE
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email])
    msg.body = f"""To reset your password follow this link:
{url_for('users.reset', token=token, _external=True)}

If you ignore this email no changes will be made
"""
    mail.send(msg)


@users.route('/forgot_password', methods=['GET','POST']) #<---HERE
def forgot():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if request.method == 'POST':
        formDict = request.form.to_dict()
        if formDict.get('submit_button'):
            user = Users.query.filter_by(email = formDict.get('email')).first()
            send_reset_email(user)
            print('user::',user)
            print('an email has been sent to your email with reset instructions')
            return redirect(url_for('users.login'))
    return render_template('forgot.html')

@users.route('/reset_password/<token>', methods=['GET','POST']) #<---HERE
def reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user = Users.verify_reset_token(token)
    if user is None:
        print('Invalid token')
        return redirect(url_for('users.forgot'))
    
    if request.method == 'POST':
        formDict = request.form.to_dict()
        user.password = formDict.get('password')
        db.session.commit()
        return render_template_string("Your password has been updated!")
    return render_template('reset_password.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if request.method == 'POST':
        formDict = request.form.to_dict()
        user = Users(email=formDict.get('email'),password=formDict.get('password'))
        db.session.add(user)
        db.session.commit()
    return render_template('register.html')

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    if request.method == 'POST':
        formDict = request.form.to_dict()
        user = Users.query.filter_by(email=formDict.get('email')).first()
        if user:
            login_user(user)
            return redirect(url_for('users.home'))
    return render_template('login.html')


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))