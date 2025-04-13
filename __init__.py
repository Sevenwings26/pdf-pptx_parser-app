from flask import Flask
from extensions import db, api, cache
from config import SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, SECRET_KEY, CACHE_TYPE, CACHE_REDIS_URL



def create_app():
    app = Flask(__name__)

    # ✅ Set app config before initializing cache
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_FILE_SIZE'] = MAX_FILE_SIZE
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['CACHE_TYPE'] = CACHE_TYPE  # ✅ Ensure CACHE_TYPE is set
    app.config['CACHE_REDIS_URL'] = CACHE_REDIS_URL

    # ✅ Initialize cache after setting configurations
    cache.init_app(app)
    db.init_app(app)

    # Register blueprints
    from api.routes import api_ns
    from web.routes import web_bp

    app.register_blueprint(web_bp)
    api.init_app(app)
    api.add_namespace(api_ns)

    return app
