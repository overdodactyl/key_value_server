docker build -t key-value-store .

docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest

docker run -d -p 8081:8080 -e INSTANCE_ID=KVStore1 key-value-store
docker run -d -p 8082:8080 -e INSTANCE_ID=KVStore2 key-value-store
docker run -d -p 8083:8080 -e INSTANCE_ID=KVStore3 key-value-store

sleep 10

python benchmark.py