# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV CRAWLER_START_URL=https://www.roesrath.de/
ENV CRAWLER_DEPTH=2
ENV DB_CONNECTION_STRING=postgresql://santa:claus@localhost:5432/postgres
ENV KEYWORDS_MIN_LENGTH=4
ENV KEYWORDS_MAX_AMOUNT=60

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 5000
# Command to run the application
CMD ["python", "app.py"]