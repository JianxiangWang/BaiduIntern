# encoding: utf-8

#  获取
# "视频",
# "评测",
# "简介",
# "个人资料"
# 的预测结果
def main(predict_file, to_file):

    with open(predict_file) as fin, open(to_file, "w") as fout:
        for line in fin:
            url, s, p, o, _ = line.strip().split("\t")
            if p in ["视频", "评测", "简介", "个人资料"]:
                fout.write(line)

# 获取 "视频", "评测", "简介", "个人资料" 的预测结果中的title
def get_someP_title(in_file, to_file):

    with open(in_file) as fin, open(to_file, "w") as fout:
        for line in fin:
            url, s, p, o, _ = line.strip().split("\t")
            fout.write(s + "\n")


if __name__ == '__main__':
    # main(
    #     "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo",
    #     "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP"
    # )

    get_someP_title(
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.title"
    )

