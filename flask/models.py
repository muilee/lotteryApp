from main import db

class Todo(db.Model):
	# __table__name = 'user_table'，若不寫則看 class name
    # 設定 primary_key
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(80))

	def __init__(self, content):
		self.content = content
	def __repr__(self):
		return "<Todo %r>"%self.content