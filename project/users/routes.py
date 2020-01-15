from flask import Blueprint, render_template
# from flask_login import login_user, current_user, logout_user, login_required
from flask_login import login_user
from project import db, bcrypt
from .forms import LoginForm, RegistrationForm
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
