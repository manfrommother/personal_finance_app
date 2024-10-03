from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', 
                                   choices=[('income', 'Income'), ('expense', 'Expense')], 
                                   validators=[DataRequired()])
    submit = SubmitField('Add Transaction')