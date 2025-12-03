# Use a Python base image (Debian based is easier for Tesseract)
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies, including Tesseract OCR and image libraries
# Tesseract requires language data, which is included in tesseract-ocr
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (Render will handle mapping the external port)
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
