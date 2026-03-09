# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
# All versions are specified in requirements.txt (including transitive deps)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.app
ENV FLASK_ENV=development

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
