# Use Python runtime as a base image
FROM python:3.12.4

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your application runs on
EXPOSE 80

# Specify the command to run your application
CMD ["python3", "modules/main.py"]
