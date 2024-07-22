# Gunakan image dasar Python
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV dan library lainnya
RUN pip install --no-cache-dir \
    opencv-python-headless \
    numpy \
    flask

# Set working directory
WORKDIR /app

# Salin file ke dalam image
COPY . /app

# Expose port untuk Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
