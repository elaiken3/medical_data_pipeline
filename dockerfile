# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables (only for defaults, override in docker-compose)
ENV DB_NAME=medical_records
ENV DB_USER=postgres
ENV DB_PASS=your_password_placeholder
ENV DB_HOST=db 
ENV DB_PORT=5432
ENV JWT_SECRET_KEY=your_jwt_secret_key_placeholder

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first for better caching
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it.sh script to the image
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy the rest of the application code
COPY . .  

# Run the pipeline and the API server (modified)
CMD ["/bin/sh", "-c", "/wait-for-it.sh db:5432 -- python pipeline.py && python api.py"] 
