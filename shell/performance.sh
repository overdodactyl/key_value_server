docker stop $(docker ps -q)

### Single Server
docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest
docker run -d -p 8081:8080 -e INSTANCE_ID=KVStore1 key-value-store
sleep 15
locust --csv=locust_results2/one_server --headless -t1m --users 100 --spawn-rate 2 -H http://localhost > /dev/null 2>&1

docker stop $(docker ps -q)

#### Two Servers
docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest
docker run -d -p 8081:8080 -e INSTANCE_ID=KVStore1 key-value-store
docker run -d -p 8082:8080 -e INSTANCE_ID=KVStore2 key-value-store
sleep 15
locust --csv=locust_results2/two_servers --headless -t1m --users 100 --spawn-rate 2 -H http://localhost > /dev/null 2>&1

docker stop $(docker ps -q)

#### Three Servers
docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest
docker run -d -p 8081:8080 -e INSTANCE_ID=KVStore1 key-value-store
docker run -d -p 8082:8080 -e INSTANCE_ID=KVStore2 key-value-store
docker run -d -p 8083:8080 -e INSTANCE_ID=KVStore3 key-value-store
sleep 15
locust --csv=locust_results2/three_servers --headless -t1m --users 100 --spawn-rate 2 -H http://localhost > /dev/null 2>&1