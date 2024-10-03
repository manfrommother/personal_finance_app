from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(140))
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} - {self.description}>'

    @classmethod
    def create_from_form(cls, form_data, user_id):
        category = Category.query.filter_by(name=form_data['category']).first()
        if not category:
            category = Category(name=form_data['category'])
            db.session.add(category)
            db.session.flush()  # This will assign an ID to the category if it's new
        
        return cls(
            amount=float(form_data['amount']),
            description=str(form_data['description']),
            type=str(form_data['transaction_type']),
            user_id=int(user_id),
            category_id=category.id
        )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
