FROM python:3.10.12

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    ffmpeg \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Change this line to ensure it points to the correct requirements file
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "modules/main.py"]
