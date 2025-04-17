from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_caching import Cache
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


cache = Cache()
db = SQLAlchemy()

api = Api(
    version='1.0',
    title='File Parser API',
    description='API Endpoints for the PDF/PPTx Parser.',
    doc='/api/docs/'  # This is the documentation URL
)

celery = Celery(
    __name__,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

