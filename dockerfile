# Use the official lightweight Python image
FROM python:3.11-slim


ENV DB_HOST=localhost 
ENV DB_NAME=ucare
ENV DB_USER=admin123
ENV DB_PASS=admin123 
ENV DB_PORT=5432
ENV API_KEY=your_api_key_here
ENV PROVIDER=your_provider_here

# Set the working directory
WORKDIR /app

# # Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-server-dev-all \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt /app

# Update pip first
RUN pip install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]