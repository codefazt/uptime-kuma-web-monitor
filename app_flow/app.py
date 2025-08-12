from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_flow.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app_flow.routes import auth_routes, token_routes
app.register_blueprint(auth_routes.bp)
app.register_blueprint(token_routes.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
