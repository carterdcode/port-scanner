# minimal Python image
FROM python:3.11-slim

# Set the working dir
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your src into container
COPY src/ ./src

# Set the working dir
WORKDIR /app/src

# Set entrypoint to behave like command line program (allows you to enter IP when running it)
ENTRYPOINT ["python", "port-scanner.py"]

