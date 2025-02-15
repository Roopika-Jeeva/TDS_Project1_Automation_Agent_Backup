# Use Python as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract OCR (for image processing)
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Install Node.js, npm, and Prettier (Pinned to 3.4.2)
RUN apt update && apt install -y nodejs npm
RUN npm install -g prettier@3.4.2


# Expose the port for Flask
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
