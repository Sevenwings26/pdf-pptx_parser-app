# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose the port Flask runs on
EXPOSE 5000

# Run database migrations (if using Flask-Migrate)
# RUN flask db upgrade

# Start the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

