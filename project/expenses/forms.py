from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


MONTHS = (
	(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
	(5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
	(9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
)


class AddMonthForm(FlaskForm):
	year = IntegerField('Year', validators=[NumberRange(min=1900, max=2500)])
	month = SelectField('Month', validators=[DataRequired()], choices=MONTHS, coerce=int)
	submit = SubmitField('Add new')
