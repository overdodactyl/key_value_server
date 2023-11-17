# Use a specific version of Alpine Linux
FROM python:3.9-alpine3.14

# Set the working directory inside the container
WORKDIR /app

# Install gcc, Python development headers, Linux headers, and standard C library headers
RUN apk add --no-cache gcc python3-dev linux-headers musl-dev

# Create a non-root user
RUN adduser -D myuser

# Set ownership of the application directory to the non-root user
RUN chown -R myuser:myuser /app

# Install dependencies
COPY requirements_kv_server.txt /app
RUN pip install -r requirements_kv_server.txt

COPY key_value_server.py /app

# Combine commands to reduce layers
RUN mkdir -p /app/logs /app/data && \
    chmod 777 /app/logs && \
    mkdir -p /app/data && \
    chmod 777 /app/data && \
    apk del gcc python3-dev linux-headers musl-dev && \
    rm -rf /var/cache/apk/*

# Expose the port your server is listening on
EXPOSE 8080

# Switch to the non-root user
USER myuser

# We use Uvicorn to serve the FastAPI app
CMD ["uvicorn", "key_value_server:app", "--host", "0.0.0.0", "--port", "8080"]
