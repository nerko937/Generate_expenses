from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash
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
		return redirect(url_for('expenses.main'))
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

@expenses.route("/delete_month/<month_id>", methods=['GET'])
@login_required
def delete_month(month_id):
	month = Month.query.filter_by(id=month_id).first()
	if month.user_id == current_user.id:
		db.session.delete(month)
		db.session.commit()
		flash('Month has been deleted!', 'success')
		return redirect(url_for('expenses.main'))
	else:
		flash("You cant delete month that doesn't belongs to you!", 'dange')
		return redirect(url_for('expenses.main'))
