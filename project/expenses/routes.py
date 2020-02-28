from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from project import db
from .models import Month, Expense
from .forms import MONTHS, CATEGORIES, AddMonthForm, AddExpenseForm, UpdateExpenseForm


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
	month = Month.query.filter_by(id=month_id).first_or_404()
	if month.user_id == current_user.id:
		db.session.delete(month)
		db.session.commit()
		flash('Month has been deleted!', 'success')
		return redirect(url_for('expenses.main'))
	else:
		flash("You can't delete month that doesn't belongs to you!", 'danger')
		return redirect(url_for('expenses.main'))

@expenses.route('/month/<month_id>', methods=['GET', 'POST'])
@login_required
def month(month_id):
	month = Month.query.filter_by(id=month_id).first_or_404()
	add_form = AddExpenseForm()
	if add_form.submit_add.data and add_form.validate():
		expense = Expense(
			amount=add_form.amount.data, category=add_form.category.data,
			description=add_form.description.data, month_id=month_id
		)
		db.session.add(expense)
		db.session.commit()
		return redirect(url_for('expenses.month', month_id=month.id))
	update_form = UpdateExpenseForm()
	if update_form.submit_update.data and update_form.validate():
		expense = Expense.query.filter_by(id=update_form.expense_id.data).first()
		
		expense.amount = update_form.amount.data
		expense.category = update_form.category.data
		expense.description = update_form.description.data
		db.session.commit()
		return redirect(url_for('expenses.month', month_id=month.id))
	if month.user_id == current_user.id:
		ROUTE_CATEGORIES = [el[1] for el in CATEGORIES]
		total = db.session.query(db.func.sum(Expense.amount)).filter_by(month_id=month_id)
		totals = {key: str(total.filter_by(category=key).first()[0]) for key in ROUTE_CATEGORIES}
		totals['Total'] = str(total.first()[0])
		return render_template(
			'month.html', title='Expenses', month=month, totals=totals,
			add_form=add_form, update_form=update_form
		)
	else:
		flash("You can't view a month that doesn't belongs to you!!", 'danger')
		return redirect(url_for('expenses.main'))

@expenses.route("/delete_expense/<expense_id>", methods=['GET'])
@login_required
def delete_expense(expense_id):
	expense = Expense.query.filter_by(id=expense_id).first_or_404()
	month = Month.query.filter_by(id=expense.month_id).first()
	if month.user_id == current_user.id:
		db.session.delete(expense)
		db.session.commit()
		flash('Expense has been deleted!', 'success')
		return redirect(url_for('expenses.month', month_id=month.id))
	else:
		flash("You can't delete expense that doesn't belongs to you!", 'danger')
		return redirect(url_for('expenses.month', month_id=month.id))
