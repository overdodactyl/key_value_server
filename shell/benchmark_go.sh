docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest

docker run -d -p 8081:8080 overdodactyl/kv_server_go:latest
docker run -d -p 8082:8080 overdodactyl/kv_server_go:latest
docker run -d -p 8083:8080 overdodactyl/kv_server_go:latest

sleep 10

source venv/bin/activate
python benchmark.py