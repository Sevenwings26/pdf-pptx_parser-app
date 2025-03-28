from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery = Celery(
    __name__,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)

def make_celery(app):
    celery.conf.update(app.config)
    return celery

@celery.task
def process_file(file_path):
    """Delegates parsing to the correct function."""
    from parser import extract_pdf_data, extract_pptx_data
    
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


