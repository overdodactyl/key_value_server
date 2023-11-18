#go mod init mykeyvaluestore


docker build -f Dockerfile_go -t mykeyvaluestore .

#docker run -p 8080:8080 mykeyvaluestore

docker build -t kv_server_go .

docker tag kv_server_go overdodactyl/kv_server_go:$VERSION
docker tag kv_server_go overdodactyl/kv_server_go:latest

docker push overdodactyl/kv_server_go:$VERSION
docker push overdodactyl/kv_server_go:latest