from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from parser import extract_pdf_data, extract_pptx_data


celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,  # Critical for Docker
    broker_connection_retry=True,
    broker_connection_max_retries=3
)

def make_celery(app):
    celery.conf.update(app.config)
    return celery


@celery.task
def process_file(file_path):
    """Delegates parsing to the correct function."""
    
    file_ext = file_path.rsplit('.', 1)[1].lower()
    if file_ext == "pdf":
        content, error = extract_pdf_data(file_path)
    elif file_ext == "pptx":
        content, error = extract_pptx_data(file_path)
    else:
        return "Unsupported file type"

    if error:
        return f"Error: {error}"    
    return f"Successfully processed {file_path}"

