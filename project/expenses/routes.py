from datetime import date
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from project import db
from .models import Month
from .forms import MONTHS, AddMonthForm


expenses = Blueprint('expenses', __name__, template_folder='templates')

@expenses.route("/", methods=['GET', 'POST'])
@login_required
def main():
	form = AddMonthForm()
	if form.validate_on_submit():
		month = Month(year=form.year.data, month=form.month.data, user_id=current_user.id)
		db.session.add(month)
		db.session.commit()
		redirect(url_for('expenses.main'))
	user_months = Month.query.filter_by(
		user_id=current_user.id).order_by(Month.year.desc(), Month.month.asc()
	)
	TODAY = date.today()
	CURRENT_MONTH = TODAY.month
	CURRENT_YEAR = TODAY.year
	MONTH_LIST = [month[1] for month in MONTHS]
	return render_template(
		'main.html', title='Homepage', user_months=user_months, form=form,
		months=MONTH_LIST, cr_month=CURRENT_MONTH, cr_year=CURRENT_YEAR
	)
