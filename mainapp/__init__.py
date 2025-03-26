from flask import Flask
from extensions import db, api
from config import SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, SECRET_KEY

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_FILE_SIZE'] = MAX_FILE_SIZE
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from api.routes import api_ns
    from web.routes import web_bp
    
    app.register_blueprint(web_bp)
    api.init_app(app)
    api.add_namespace(api_ns)
    
    return app

    # def create_app():
    # app = Flask(__name__)
    # # ... other config ...
    
    # # Register blueprints - WEB FIRST
    # from .web.routes import web_bp
    # from .api.routes import api_bp
    
    # app.register_blueprint(web_bp)  # Web interface at /
    # api.init_app(app)
    # api.add_namespace(api_bp)      # API at /api
    
    # return app