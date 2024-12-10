from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_company = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    company = db.relationship('User', backref='jobs')

    def __repr__(self):
        return f'<Job {self.title}>'
