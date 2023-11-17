# Use a lightweight Linux distribution with Python installed
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app

# Install gcc, Python development headers, Linux headers, and standard C library headers
RUN apk add --no-cache gcc python3-dev linux-headers musl-dev

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy your application files into the container
COPY key_value_server.py /app

# Create directories for logs and data
RUN mkdir /app/logs
RUN mkdir /app/data

# Set environment variable
ENV INSTANCE_ID=Instance1

# Expose the port your server is listening on
EXPOSE 8080

# Define the command to run when the container starts
CMD ["python", "-u", "key_value_server.py"]
