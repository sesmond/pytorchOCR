#!/bin/bash

# 定义 训练需要的相关函数
function get_train_cmd {
  printf "选择您要训练的模型："
  select var in "检测" "识别"; do
    break;
  done
  echo "您选择了： $var  "
  Date=$(date +%Y%m%d%H%M)
  RTN_CMD=""
  if [ "$var" = "检测" ]; then
      select dnet in "DB" "PSE" "PAN" "SAST"; do
          break;
      done
      case $dnet in
        "DB" )
           select dbackbone in "mobilev3" "resnet50" "resnet50_3_3"; do
                break;
            done
          ;;
        "PSE" )
         select dbackbone in "mobilev3" "resnet50" "resnet50_3_3"; do
                break;
            done
          ;;
        "PAN" )
          select dbackbone in "mobilev3" "resnet50" "resnet50_3_3"; do
                  break;
              done
            ;;
        "SAST" )
        select dbackbone in "mobilev3" "resnet50" "resnet50_3_3"; do
                break;
            done
          ;;
        "*" )
          echo "选择错误！"
          exit
          ;;
      esac
      config_file="./config/det_${dnet}_${dbackbone}.yaml"
      echo "配置文件："$config_file
#      read -p "输入训练要用的GPU:" gpus ;
#      echo "您选择了GPU $gpus 进行训练"
#      set -x
      RTN_CMD=" python -m tools.det_train \
        --config $config_file \
        --log_str "logs" \
        --n_epoch 1200 \
        --start_val 600 \
        --base_lr 0.002 \
         >> ./logs/det_train_$Date.log 2>&1 &"
#         shell的function只能返回整数值,字符串只能通过变量返回
      return 0
  fi

  if [ "$var" = "识别" ]; then
      echo "停止训练"
      ps aux|grep python|grep name=psenet|awk '{print $2}'|xargs kill -9
      exit
  fi
}
