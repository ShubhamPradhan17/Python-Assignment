from flask import Flask
from flask_jwt_extended import JWTManager
from routes.books import books_bp
from routes.members import members_bp
from routes.transaction import transactions_bp
from routes.auth import auth_bp
from routes.reports.report import report_bp


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'my_secret_key' 
jwt = JWTManager(app)

app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(report_bp)

if __name__ == '__main__':
    app.run(debug=True)
