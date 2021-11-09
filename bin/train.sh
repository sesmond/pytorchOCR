. bin/function_train.sh
get_train_cmd
read -p "输入训练要用的GPU:" gpus ;
echo "您选择了GPU $gpus 进行训练"
_TRAIN_STR="CUDA_VISIBLE_DEVICES=$gpus nohup ${RTN_CMD}"
echo "训练脚本：$_TRAIN_STR"
eval "$_TRAIN_STR"
exit
