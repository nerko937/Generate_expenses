from datetime import date
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from project import db
from .models import Month


expenses = Blueprint('expenses', __name__, template_folder='templates')

@expenses.route("/", methods=['GET', 'POST'])
@login_required
def main():
	# form = LoginForm()
	MONTHS = (
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 
		'August', 'September', 'October', 'November', 'December'
	)
	# if form.validate_on_submit():
	# 	user = User.query.filter_by(email=form.email.data).first()
	# 	if user and bcrypt.check_password_hash(user.password, form.password.data):
	# 		login_user(user, remember=form.remember.data)
	# 		return 'Logged successfuly'
	# 	else:
	# 		return 'Login failed'
	# 		# next_page = request.args.get('next')
    #         # return redirect(next_page) if next_page else redirect(url_for('main.home'))
    #     # else:
    #     #     flash('Login Unsuccessful. Please check email and password', 'danger')
	user_months = Month.query.filter_by(user_id=current_user.id).order_by(Month.year.desc(), Month.month.asc())
	TODAY = date.today()
	CURRENT_MONTH = TODAY.month
	CURRENT_YEAR = TODAY.year
	# return render_template('main.html', title='Homepage', form=form, months=user_months)
	return render_template(
		'main.html', title='Homepage',
		user_months=user_months, months=MONTHS, cr_month=CURRENT_MONTH, cr_year=CURRENT_YEAR
	)
