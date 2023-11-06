# Use a lightweight Linux distribution with Python installed
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app
# Create a directory for logs


# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy your application files into the container
COPY key_value_server.py /app

RUN mkdir /app/logs
RUN mkdir /app/data

ENV INSTANCE_ID=Instance1

# Expose the port your server is listening on
EXPOSE 8080

# Define the command to run when the container starts
CMD ["python", "-u", "key_value_server.py"]
