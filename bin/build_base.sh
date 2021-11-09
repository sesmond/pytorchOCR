# build docker
if [ "$1" == "proxy" ]; then
    echo "Run build docker image with proxy"
    docker build \
        --network host \
        --build-arg http_proxy="http://172.17.0.1:8123" \
        --build-arg https_proxy="http://172.17.0.1:8123" \
        --build-arg HTTP_PROXY="http://172.17.0.1:8123" \
        --build-arg HTTPS_PROXY="http://172.17.0.1:8123" \
        -f deploy/Dockerfile \
        -t opencv-docker-base:v1 .
    exit
fi

docker build -f deploy/Dockerfile -t opencv-docker-base:v1 .