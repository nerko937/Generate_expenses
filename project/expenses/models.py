from project import db


class Expense(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(150), nullable=False)
	amount = db.Column(db.Numeric(6, 2))
	month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)
	description = db.Column(db.Text())
	short_descr = db.Column(db.String(83), nullable=True)
	has_short_descr = db.Column(db.Boolean(), default=False, nullable=False)

	def __repr__(self):
		return f"Expense('{self.id}', '{self.amount}')"
	
	def __init__(self, **kwargs):
		super(Expense, self).__init__(**kwargs)
		if self.description and len(self.description) > 80:
			self.short_descr = self.description[:80] + '...'
			self.has_short_descr = True


class Month(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	month = db.Column(db.Integer, nullable=False)
	year = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	expenses = db.relationship(
		'Expense', backref='month_related', lazy=True,
		cascade='all, delete-orphan', order_by=('Expense.category')
	)

	def __repr__(self):
		return f"Month('{self.id}', '{self.month}-{self.year}')"
