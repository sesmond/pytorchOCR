# 使用docker训练
#!/bin/bash

if [ "$1" == "stop" ]; then
    echo "关闭OCR训练容器..."
    docker ps|grep ocr_train|awk '{print $1}'|xargs docker stop
    exit
fi

. bin/function_train.sh
get_train_cmd
CMD_STR=$RTN_CMD
echo "训练命令：$CMD_STR"


PWD=`pwd`
ROOT_DATA=/app/data/
GPU_OPT="--runtime=nvidia"
DAEMON=""
PROXY=""
PROXY="--env http_proxy=http://172.17.0.1:8123 --env https_proxy=http://172.17.0.1:8123 --env HTTP_PROXY=http://172.17.0.1:8123 --env HTTPS_PROXY=http://172.17.0.1:8123"

read -p "输入训练要用的GPU(3代表CPU):" gpus ;
echo "您选择了GPU $gpus 进行训练"
if [ "$gpus" == "3" ]; then
    echo "本地（笔记本上，无显卡）调试模式 ..."
    GPU_OPT=""
    PROXY=""
else
    echo "启动训练，模式：GPU"
    DAEMON="-d"
fi


# docker -v 挂载目录
FULL_CMD="
    docker run --rm
    -it $DAEMON $GPU_OPT
    -e NVIDIA_VISIBLE_DEVICES=$gpus $PROXY
    -v $PWD:/home/pytorchOCR
    -v $ROOT_DATA:$ROOT_DATA
    -v /root/.cache:/root/.cache
    --name ocr_train
    --network host
    --workdir /home/pytorchOCR
    opencv-docker-base:v2
    $CMD_STR
"

echo "启动命令："
echo "==================================="
echo "$FULL_CMD"
echo "==================================="
eval $FULL_CMD

#docker run -itd -v $PWD:/home/pytorchOCR \
#-v /Users/minjianxu/Documents/ocr_data/icdar2015/:/Users/minjianxu/Documents/ocr_data/icdar2015/ \
#--privileged=true opencv-docker-base:v2 /bin/bash