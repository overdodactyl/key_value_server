VERSION=1.1

# Build the Docker image
docker build -t kv_server .

# Tag the image with the specific version
docker tag kv_server overdodactyl/kv_server:$VERSION

# Also tag the same image as 'latest'
docker tag kv_server overdodactyl/kv_server:latest

# Push the version-specific tag to Docker Hub
docker push overdodactyl/kv_server:$VERSION

# Push the 'latest' tag to Docker Hub
docker push overdodactyl/kv_server:latest
