from app import create_app, db
from app.models import User, Transaction, Category, Budget

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 'Category': Category, 'Budget': Budget}

if __name__ == '__main__':
    app.run(debug=True)