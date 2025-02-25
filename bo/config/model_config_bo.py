# class DetConfigBase:
#     gpu_id = '0'  # 设置训练的gpu id，多卡训练设置为 '0,1,2'
#     algorithm = DB  # 算法名称
#     pretrained = True  # 是否加载预训练
#     in_channels = [256, 512, 1024, 2048]  #
#     inner_channels = 256  #
#     k = 50
#     adaptive = True
#     crop_shape = [640, 640]  # 训练时crop图片的大小
#     shrink_ratio = 0.4  # kernel向内收缩比率
#     n_epoch = 1200  # 训练的epoch
#     start_val = 400  # 开始验证的epoch，如果不想验证直接设置数值大于n_epoch
#     show_step = 20  # 设置迭代多少次输出一次loss
#     checkpoints =./ checkpoint  # 保存模型地址
#     save_epoch = 100  # 设置每多少个epoch保存一次模型
#     restore = False  # 是否恢复训练
#     restore_file =./ DB.pth.tar  # 恢复训练所需加载模型的地址
#
#
# class FunctionConfig:
#     function = ""
#
#
# class LossConfig:
#     function = ptocr.model.loss.db_loss, DBLoss
#     l1_scale = 10
#     bce_scale = 1
#
#
# class OptimizerConfig:
#     function = ptocr.optimizer, SGDDecay
#     base_lr = 0.002
#     momentum = 0.99
#     weight_decay = 0.0005
#
#
# class OptimizerDecayConfig:
#     function = ptocr.optimizer, adjust_learning_rate_poly
#     factor = 0.9
#
#
# class DetConfig:
#     base = DetConfigBase
#
#     backbone = FunctionConfig
#
#     head = FunctionConfig
#     #  function= ptocr.model.head.det_FPEM_FFM_Head,FPEM_FFM_Head
#     #  function= ptocr.model.head.det_FPNHead,FPN_Head
#
#     segout = FunctionConfig
#
#     architectures =
#     model_function = ptocr.model.architectures.det_model, DetModel
#     loss_function = ptocr.model.architectures.det_model, DetLoss
#
#
#     loss = LossConfig
#
#     optimizer = OptimizerConfig
#
#     optimizer_decay = OptimizerDecayConfig
#
#
#     trainload =
#         function = ptocr.dataloader.DetLoad.DBProcess, DBProcessTrain
#         train_file = / src / notebooks / detect_text / icdar2015 / train_list.txt
#         num_workers = 10
#         batch_size = 8
#
#     testload =
#         function = ptocr.dataloader.DetLoad.DBProcess, DBProcessTest
#         test_file = / src / notebooks / detect_text / icdar2015 / test_list.txt
#         test_gt_path = / src / notebooks / detect_text / icdar2015 / ch4_test_gts /
#         test_size = 736
#         stride = 32
#         num_workers = 5
#         batch_size = 4
#
#     postprocess =
#         function = ptocr.postprocess.DBpostprocess, DBPostProcess
#         is_poly = False  # 测试时，检测弯曲文本设置成 True，否则就是输出矩形框
#         thresh = 0.5
#         box_thresh = 0.6
#         max_candidates = 1000
#         unclip_ratio = 2
#         min_size = 3
#
#     infer = 
#         model_path = './checkpoint/ag_DB_bb_resnet50_he_DB_Head_bs_8_ep_1200_bk/DB_best.pth.tar'
#         path = '/src/notebooks/detect_text/icdar2015/ch4_test_images'
#         save_path = './result'
