from decimal import ROUND_HALF_EVEN
from flask_wtf import FlaskForm
from wtforms import (
	IntegerField, SelectField, SubmitField, DecimalField, StringField, HiddenField
)
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea


MONTHS = (
	(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
	(5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
	(9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
)

CATEGORIES = (
	('Bills', 'Bills'), ('Entertainment', 'Entertainment'), ('Food', 'Food')
)


class AddMonthForm(FlaskForm):
	year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1900, max=2500)])
	month = SelectField('Month', validators=[DataRequired()], choices=MONTHS, coerce=int)
	submit = SubmitField('Add new')


class ExpeneFormMixin():
	amount = DecimalField(
		'Amount',
		places=2,
		rounding=ROUND_HALF_EVEN,
		validators=[
			DataRequired(), NumberRange(min=0.01, max=999999.99)
		]
	)
	category = SelectField(
		'Category', validators=[DataRequired()], choices=CATEGORIES
	)
	description = StringField('Description', widget=TextArea())


class AddExpenseForm(FlaskForm, ExpeneFormMixin):
	submit_add = SubmitField('Save')


class UpdateExpenseForm(FlaskForm, ExpeneFormMixin):
	submit_update = SubmitField('Save')
	expense_id = HiddenField('Expense ID', id='update-id')
