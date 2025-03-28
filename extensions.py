from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_caching import Cache


cache = Cache()
db = SQLAlchemy()

api = Api(
    version='1.0',
    title='File Parser API',
    description='API Endpoints for the PDF/PPTx Parser.',
    doc='/api/docs/'  # This is the documentation URL
)

