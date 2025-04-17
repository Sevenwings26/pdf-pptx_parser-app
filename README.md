# PDF/PPTX Parsing APP

## Overview
This project provides a web application and API endpoints that allow users to upload PDF and PPTX files, extract their contents, and process them asynchronously using Celery, and .xslx file to csv converter. It includes a structured deployment with Docker Compose, featuring an API Gateway, Parsing Service, Database Service, and Redis for task queuing.

## Features
- Secure file upload (PDF & PPTX only)
- Asynchronous processing with Celery
- File parsing and content extraction
- Database storage for uploaded files and parsed content
- Dockerized deployment with API Gateway, Parsing Service, and Database
- Redis for caching and message brokering (optional RabbitMQ support)

## Tech Stack
- **Backend:** Flask
- **Task Queue:** Celery
- **Message Broker:** Redis (or RabbitMQ)
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose

## Installation
### Prerequisites
- Python 3.x
- Docker & Docker Compose
- Redis (if using Celery)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Sevenwings26/pdf-pptx_parser-app.git
   cd pdf-pptx_parser-app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate`   # On Mac: source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Configure your `.env` file accordingly.
4. Run the application:
   ```bash
   python run.py
   ```

## Running with Docker Compose
1. Build and start services:
   ```bash
   docker-compose up --build
   ```
2. The application should be available at `http://127.0.0.1:5000`

## API/WEB Endpoints 
### for Parsing (don't api to the web route)
| Method | Endpoint | Description |
|--------|-------------|----------------|
| `GET` | `/` | Landing page |
| `POST` | `/api/upload` | Upload a PDF/PPTX file |
| `GET` | `/api/uploaded_files` | List recent uploads |
| `GET` | `/api/parsed_files` | Retrieve all parsed files |
| `GET` | `/api/parsed_files/{file_id}` | Retrieve a specific file |
| `DELETE` | `/files/<id>` | Delete a specific file |
<!-- | `GET` | `/tasks/<task_id>` | Check Celery task status | -->
### for converting .xslx to csv
| Method | Endpoint | Description |
|--------|-------------|----------------|
| `POST` | `/convert_to_csv` | Upload xlsx file |
| `GET` | `/download/{filename}` | Download converted file


## Celery & Background Processing
1. Start Redis:
   ```bash
   docker run -d -p 6379:6379 redis
   ```
2. Start the Celery worker:
   ```bash
   celery -A app.celery worker --loglevel=info
   ```
3. Submit a task:
   ```python
   from app.tasks import process_file
   process_file.delay("example.pdf")
   ```

## Deployment
For production deployment, you can use:
```bash
Docherfile docker-compose.yml
```

## License
This project is licensed under the MIT License.

