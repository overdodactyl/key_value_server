# Use a lightweight Linux distribution with Python installed
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app
# Create a directory for logs
RUN mkdir /app/logs

# Copy your application files into the container
COPY key_value_server.py /app
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your server is listening on
EXPOSE 8080-8083

# Define the command to run when the container starts
CMD ["python", "key_value_server.py"]