from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import TransactionForm
from app.models import Transaction, Category
import logging

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('index.html', title='Home', transactions=transactions)

@bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        logging.info(f"Form data: {form.data}")
        try:
            transaction = Transaction.create_from_form(form.data, current_user.id)
            db.session.add(transaction)
            db.session.commit()
            flash('Your transaction has been added!')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding transaction: {str(e)}")
            flash(f'Error adding transaction: {str(e)}', 'error')
    return render_template('add_transaction.html', title='Add Transaction', form=form)