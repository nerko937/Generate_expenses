from flask import Blueprint, render_template, redirect, url_for
# from flask_login import login_user, current_user, logout_user, login_required
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from project import db, bcrypt, mail
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, RequestResetForm, ResetPasswordForm
from .models import User


users = Blueprint('users', __name__, template_folder='templates')

@users.route("/login", methods=['GET', 'POST'])
def login():
	# if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return 'Logged successfuly'
		else:
			return 'Login failed'
			# next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('main.home'))
        # else:
        #     flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route("/register", methods=['GET', 'POST'])
def register():
	# if current_user.is_authenticated:
	#     return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		# flash('Your account has been created! You are now able to log in', 'success')
		# return redirect(url_for('users.login'))
		return 'Successfuly registered'
	return render_template('reqister.html', title='Register', form=form)

@users.route("/logout")
def logout():
	logout_user()
	return 'Successfuly logged out'
	# return redirect(url_for('users.login'))

@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
		current_user.password = hashed_password
		db.session.commit()
		return 'Successfuly changed password'
		# next_page = request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('main.home'))
        # else:
        #     flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('change_password.html', title='Change password', form=form)

@users.route("/request_password_reset", methods=['GET', 'POST'])
def request_reset():
	# if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		token = user.get_reset_token()
		msg = Message('Password Reset Request', sender='nerko938@gmail.com', recipients=[user.email])
		msg.body = f'''
To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
		mail.send(msg)
		# flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('request_reset.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
	# if current_user.is_authenticated:
	#     return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		return 'Reset failed'
		# flash('That is an invalid or expired token', 'warning')
		# return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		# flash('Your password has been updated! You are now able to log in', 'success')
		# return redirect(url_for('users.login'))
		return 'Password changed'
	return render_template('reset_password.html', title='Reset Password', form=form)
