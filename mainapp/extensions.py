from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
# api = Api(version='1.0', title='File Parser API', 
#           description='API for parsing files')

api = Api(
    version='1.0',
    title='File Parser API',
    description='API Documentation',
    doc='/api/docs/'  # This is the documentation URL
)