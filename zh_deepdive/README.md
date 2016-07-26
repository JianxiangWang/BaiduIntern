使用DeepDive进行中文SPO的预测

1. backup: 一些备份

2. data: 数据存储文件

3. obtain_test_data: 用于获取test数据集
    0_format_to_depparser_input: 原始句子格式化成depparser的输入
    1_run_depparser: 运行 depparser 程序
    2_format_to_so_recognizer_input: 将depparser的输出,格式化成so识别的输入
    3_run_so_recognizer: 运行so识别
    4_filte_sentences_label: 对so识别的结果, 按照deepdive的要求, 进行过滤和标注, 得到deepdive的输入

4. obtain_train: 之前版本的获取训练集,不用管他

5. obtain_train_new: 最新版本的获取训练集
    0_get_random_parts: 随机选择100个part
    1_format_to_so_recognizer_input: 格式化成so识别的输入
    2_run_so_recognizer: 运行so识别
    3_filte_sentences_label: 对so识别的结果, 按照deepdive的要求, 进行过滤和标注, 得到deepdive的输入
    4_statistics: 统计标注的结果, 即: 每个P有多少个正负样本
    5_postprocessing: 之前由于正样本少, 所以采用了一些后处理, 但是后面数据较大,没有使用这一块
    6_sample: 对3_filte_sentences_label的结果数据进行采样

6. relations: 用于DeepDive的一些代码
    (1). models: 每个P的模型都放于这个下面,对应于里面的一个文件夹

    (2). template_label: 用于生成每个P的模版
        input: 输入数据对应的文件夹
        udf: 用自定义函数文件夹
        udf/extract_so_features.py: 抽取特征
        app.ddlog: deepdive系统的配置文件
        db.url: 数据库配置文件
        deepdive.conf: deepdive系统的配置文件, 里面指明了哪些样本用于测试
        evaluation.py: 评估脚本
        load_data.py: 从大的数据文件,加载对应P的训练和测试数据
        load_data_top_negative.py: 选择负得分最大的前几个, 当前系统没用使用该脚本
        P: 里面存储当前模型对应的P
        predict.json: 在测试集合上的预测结果
        run.sh: 启动程序, 包括: 加载数据, 模型训练, 测试和得到评估结果

    (3). evaluation_result.py: 根据每个模型的预测结果, 进行整体的评估
    (4). format_seed_data.py: 种子文件格式化成json文件
    (5). 执行models下的每个模型的评估脚本
    (6). run_models.sh: 顺序运行每个模型, 也就是执行models下的每个模型的run.sh
    (7). sample_predict.py: 采样预测结果
    (8). template.py & template.sh: 根据template_label模版, 为每个P生成deepdive的模型


###############
# 程序运行方式
###############

1. 配置template_label
    (a). template_label/load_data.py
        配置训练和测试文件的路径
    (b). db.url
        配置数据库的账号和数据库地址

2. 生成对应每个P的deepdive模型
    python template.py

3. 对models文件夹下的每个P, 进行训练, 测试和评估
    sh -x run_models.sh




