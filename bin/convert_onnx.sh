python ./script/pytorch_to_onnx.py \
 --config ./config/det_PSE_mobilev3.yaml \
  --model_path checkpoint/ag_PSE_bb_mobilenet_v3_small_he_FPN_Head_bs_2_ep_50_logs/PSE_0.pth.tar \
  --img_path ./data/icdar2015/test.images/img_1.jpg \
  --save_path ./onnx/PSEnet_001.onnx --batch_size 2 --max_size 1536 --algorithm PSE --add_padding

