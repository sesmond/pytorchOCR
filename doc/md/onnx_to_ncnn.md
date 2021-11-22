#onnx模型转ncnn

##1. onnx-simplifier 消除不支持的胶水op
```
pip install -U onnx --user
pip install -U onnxruntime --user
pip install -U onnx-simplifier --user

python -m onnxsim crnn_lite_lstm_v2.onnx crnn_lite_lstm_v2-sim.onnx

```
##2. 转换为ncnn模型
```
# onnx2ncnn 是ncnn项目编译后的其中一个工具，位置在：ncnn/build-mac/tools/onnx

./onnx2ncnn pse-lite-sim.onnx pse-lite.param pse-lite.bin
./onnx2ncnn db-lite-sim.onnx db-lite.param db-lite.bin

```

##3. 验证ncnn模型推理（C++）
https://github.com/Tencent/ncnn/wiki/use-ncnn-with-alexnet.zh


参考：
- https://zhuanlan.zhihu.com/p/113338890
- https://github.com/Tencent/ncnn/issues/2026 
- https://zhuanlan.zhihu.com/p/113338890
