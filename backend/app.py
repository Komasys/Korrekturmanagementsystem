from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models.models import db
from routes.auth_bp import auth_bp
from routes.kurs_bp import kurs_bp
from routes.ticket_bp import ticket_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(kurs_bp, url_prefix='/kurs')
app.register_blueprint(ticket_bp, url_prefix='/ticket')

if __name__ == "__main__":
    app.run(debug=True)
