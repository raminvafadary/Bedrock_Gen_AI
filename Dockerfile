# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if you have any)
# For example, you might need these for PyMuPDF or other packages
# RUN apt-get update && apt-get install -y \
#     libmupdf-dev \
#     mupdf-tools \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install the specific AWS SDK versions
COPY backend/boto3-1.26.162-py3-none-any.whl backend/botocore-1.29.162-py3-none-any.whl ./
RUN pip install ./boto3-1.26.162-py3-none-any.whl ./botocore-1.29.162-py3-none-any.whl

# Copy the backend and frontend directories and other necessary files into the container
COPY backend ./backend
COPY frontend ./frontend
COPY pdfs ./pdfs

# Make sure the port used by the Streamlit app is exposed
EXPOSE 8080

# Set environment variables for AWS credentials
# IMPORTANT: It's recommended to manage these variables securely, for example, using Docker secrets or environment variables at runtime
ENV AWS_ACCESS_KEY_ID="AKIAZPHR3E6TCB7R35MM"
ENV AWS_SECRET_ACCESS_KEY="xNyriT1njumTDV1qIIyShS1N60dV+yu2F3Crq0hR"
ENV AWS_DEFAULT_REGION="us-west-2"

# If you need to mimic an AWS profile, you can create a file in the container, but be aware this is less secure
# It's better to use environment variables for AWS credentials directly
RUN mkdir -p /root/.aws && \
    echo -e "[raybdr]\naws_access_key_id = 'AKIAZPHR3E6TCB7R35MM' \naws_secret_access_key = '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'\nregion = us-west-2" > /root/.aws/credentials


# Run app.py when the container launches, specify server.address to enable connections
CMD ["streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0", "--server.port=8080"]
