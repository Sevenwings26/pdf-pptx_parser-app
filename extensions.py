from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_caching import Cache
from celery import Celery

db = SQLAlchemy()
api = Api(
    version='1.0',
    title='File Parser API',
    description='API Endpoints for the PDF/PPTx Parser.',
    doc='/api/docs/'
)
cache = Cache()  # Just initialize without config

celery = Celery(__name__)  # Also defer config


