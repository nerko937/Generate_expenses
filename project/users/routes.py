from flask import Blueprint, render_template, redirect, url_for
# from flask_login import login_user, current_user, logout_user, login_required
from flask_login import login_user, logout_user, login_required, current_user
from project import db, bcrypt
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
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
