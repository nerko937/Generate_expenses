from project import db


class Expense(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(150), nullable=False)
	amount = db.Column(db.Numeric(6, 2))
	month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)
	description = db.Column(db.Text())
	short_descr = db.Column(db.String(83), nullable=True)
	multiline_descr = db.Column(db.Text())

	def __repr__(self):
		return f"Expense('{self.id}', '{self.amount}')"
	
	def __init__(self, **kwargs):
		super(Expense, self).__init__(**kwargs)
		self.set_multiline_and_short_descr()
	
	def set_multiline_and_short_descr(self):
		if self.description and len(self.description) > 80:
			self.short_descr = self.description[:80] + '...'
			splitted = self.description.split(' ')
			for i in range(5, len(splitted), 6):
				splitted.insert(i, '<br/>')
			self.multiline_descr = ' '.join(splitted)
		else:
			self.short_descr = None
			self.multiline_descr = ''


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
