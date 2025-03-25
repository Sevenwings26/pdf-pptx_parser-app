Backend: 
● API Design: Design and implement a REST API endpoint using a Python framework 
(Please use Flask for this assessment) that accepts file uploads (PDF or PowerPoint) 
and securely saves them to a designated storage location (use the local filesystem 
for this assessment). 
● Data Parsing: Develop a module that utilizes libraries like Apache POI (for PPTX) or 
PyPDF2 (for PDF) to parse the uploaded documents. 
Extract relevant information like 
slide titles, text content, and any embedded metadata. 

● Data Storage: Implement a database schema or data model (e.g., using a relational 
database like PostgreSQL or a NoSQL database like MongoDB) to store the 
extracted information for future retrieval and analysis.

● Error Handling: Ensure robust error handling and validation to address scenarios 
such as: 
○ Unsupported file formats 
○ Corrupted files 
○ Exceeding file size limits 
○ Database connection issues 
● Deployment File: Build a deployment file using docker compose, with at least an API 
Gateway or Broker service, a Parsing service and a database Service. 
Demonstrating your knowledge of a cache service and a queuing service will be a 
plus.


Title 

Description: 

Installation 

pip install flask
pip install Werkzeug