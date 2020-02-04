from project import db


class Month(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	month = db.Column(db.Integer, nullable=False)
	year = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	expenses = db.relationship('Expense', backref='month_related', lazy=True)

	def __repr__(self):
		return f"Month('{self.id}', '{self.month}-{self.year}')"


class Expense(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(150), nullable=False)
	amount = db.Column(db.Numeric(6, 2))
	month_id = db.Column(db.Integer, db.ForeignKey('month.id'), nullable=False)
	description = db.Column(db.Text())

	def __repr__(self):
		return f"Expense('{self.id}', '{self.amount}')"
