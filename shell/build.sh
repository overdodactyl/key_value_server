VERSION=1.2

# Build the Docker image
docker build -t kv_server .

docker tag kv_server overdodactyl/kv_server:$VERSION
docker tag kv_server overdodactyl/kv_server:latest

docker push overdodactyl/kv_server:$VERSION
docker push overdodactyl/kv_server:latest
