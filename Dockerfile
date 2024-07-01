FROM python:3.10.12

# This Dockerfile Created By Mr. Ankush Yadav.  Github.com/Mswpresents
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

# Copy all files from the current directory to the working directory in the container
COPY . .

# Install Python dependencies from the Installer file
RUN pip3 install --no-cache-dir --upgrade --requirement Installer

# Set the command to run your application
CMD ["python3", "modules/main.py"]
