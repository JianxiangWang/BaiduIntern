# encoding: utf-8

def evaluate_s(org_test_data, predict_file_path):

    # 只评正例的准确与召回
    with open(org_test_data) as test_file, open(predict_file_path) as predict_file:

        # 获取预测的
        dict_predict_p_to_url_to_s = {}
        for line in predict_file:
            line_list = line.strip().split("\t")
            url = line_list[0]
            s = line_list[1]
            p = line_list[2]
            if p not in dict_predict_p_to_url_to_s:
                dict_predict_p_to_url_to_s[p] = {}
            dict_predict_p_to_url_to_s[p][url] = s

        # gold
        dict_gold_p_to_url_to_s = {}
        for line in test_file:
            line_list = line.strip().split("\t")
            p, url, s, label = line_list[0], line_list[1], line_list[2], line_list[3]

            if label == "0":
                continue

            if p not in dict_gold_p_to_url_to_s:
                dict_gold_p_to_url_to_s[p] = {}
            dict_gold_p_to_url_to_s[p][url] = s

        # 评估每个P

        for p in dict_gold_p_to_url_to_s:
            # recall
            recall_N = len(dict_gold_p_to_url_to_s[p])
            recall_M = 0
            for url in dict_gold_p_to_url_to_s[p]:
                gold_s = dict_gold_p_to_url_to_s[p][url]
                if p in dict_predict_p_to_url_to_s and url in dict_predict_p_to_url_to_s[p]:
                    pred_s = dict_predict_p_to_url_to_s[p][url]
                    if pred_s == gold_s:
                        recall_M += 1



            print p
            print "recall: %d / %d = %.4f" % (recall_M, recall_N, recall_M / float(recall_N))

if __name__ == '__main__':
    evaluate_s(
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.s",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo",
    )