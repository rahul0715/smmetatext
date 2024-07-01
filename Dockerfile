FROM python:3.10.12

# Install necessary packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    ffmpeg \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Start the bot
CMD ["python3", "modules/main.py"]
