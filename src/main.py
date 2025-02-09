import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    # Turns off default ordering of lists
    app.json.sort_keys = False

    # Configure env variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Connect the instances of the app with the different libraries
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Error handling for app
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(401)
    def unauthorised(err):
        return {"error": err.messages}, 401
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": err.messages}, 404
    
    @app.errorhandler(500)
    def internal_server(err):
        return {"error": err.messages}, 500
    
    # Register blueprints for controllers
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from controllers.club_controller import club_bp
    app.register_blueprint(club_bp)

    from controllers.book_controller import book_bp
    app.register_blueprint(book_bp)

    # Return app instance
    return app