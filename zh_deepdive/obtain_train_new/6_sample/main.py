import random

import pyprind


def get_top_n(in_file, N, to_file):

    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            if N > 0:
                fout.write(line)
            else:
                break
            N -= 1


def get_random(in_file, p, to_file):

    process_bar = pyprind.ProgPercent(12440969)
    with open(in_file) as fin, \
         open(to_file, "w") as fout:

        for line in fin:
            process_bar.update()
            if random.random() < p:
                fout.write(line)




if __name__ == '__main__':
    # get_top_n(
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label",
    #     2500000,
    #     "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_top_250w",
    # )

    get_random(
        "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label",
        0.2,
        "/home/jianxiang/pycharmSpace/BaiduIntern/zh_deepdive/data/SPO_train_data_84P_for_deepdive_label_random.0.2",
    )