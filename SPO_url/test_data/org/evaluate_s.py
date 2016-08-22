# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json



def evaluate_s(org_test_data, predict_file_path, predict_some_p_file_path):

    # 只评正例的准确与召回
    with open(org_test_data) as test_file, open(predict_file_path) as predict_file,\
            open(predict_some_p_file_path) as some_p_predict_file:

        # 获取预测的
        dict_predict_p_to_url_to_s = {}
        for line in predict_file:
            line_list = line.strip().split("\t")
            url = line_list[0]
            s = line_list[1]
            p = line_list[2]

            if p in ["视频", "评测", "简介", "个人资料", "音频", "下载"]:
                continue

            if p not in dict_predict_p_to_url_to_s:
                dict_predict_p_to_url_to_s[p] = {}
            dict_predict_p_to_url_to_s[p][url] = s

        for line in some_p_predict_file:
            line_list = line.strip().split("\t")
            url = line_list[0]
            s = line_list[1]
            p = line_list[2]

            if p not in dict_predict_p_to_url_to_s:
                dict_predict_p_to_url_to_s[p] = {}
            dict_predict_p_to_url_to_s[p][url] = s



        # gold
        dict_gold_p_to_url_to_s = {}
        dict_url_to_title = {}
        for line in test_file:
            line_list = line.strip().split("\t")
            p, url, s, label = line_list[0], line_list[1], line_list[2], line_list[3]

            if label == "0":
                continue

            if p not in dict_gold_p_to_url_to_s:
                dict_gold_p_to_url_to_s[p] = {}
            dict_gold_p_to_url_to_s[p][url] = s

            dict_url_to_title[url] = json.loads(line_list[-1])["realtitle"]

        # 评估每个P
        N = 0
        marco_precision = 0
        marco_recall = 0

        for p in dict_gold_p_to_url_to_s:

            error_cases = []
            # recall
            recall_N = len(dict_gold_p_to_url_to_s[p])
            recall_M = 0
            for url in dict_gold_p_to_url_to_s[p]:
                gold_s = dict_gold_p_to_url_to_s[p][url]
                if p in dict_predict_p_to_url_to_s and url in dict_predict_p_to_url_to_s[p]:
                    pred_s = dict_predict_p_to_url_to_s[p][url]
                    if pred_s.lower().strip() == gold_s.lower().strip():
                        recall_M += 1
                    else:
                        # print pred_s, gold_s
                        pass

            # precision
            precision_N = 0
            precision_M = 0
            for url in dict_predict_p_to_url_to_s[p]:
                pred_s = dict_predict_p_to_url_to_s[p][url]

                if p in dict_gold_p_to_url_to_s and url in dict_gold_p_to_url_to_s[p]:
                    precision_N += 1
                    gold_s = dict_gold_p_to_url_to_s[p][url]
                    if pred_s.lower().strip() == gold_s.lower().strip():
                        precision_M += 1
                    else:
                        title = dict_url_to_title[url]
                        print title, type(title)
                        error_cases.append(u"%s\t%s\t%s==>%s" % (url, title, gold_s.lower().strip(), pred_s.lower().strip()))

            N += 1
            precision = precision_M / float(precision_N)
            recall = recall_M / float(recall_N)

            marco_precision += precision
            marco_recall += recall

            print "==" * 40
            print p
            print "precision: %d / %d = %.4f" % (precision_M, precision_N, precision)
            print "recall   : %d / %d = %.4f" % (recall_M, recall_N, recall)
            print "\n".join(error_cases)
            print

        print "==" * 40
        print "marco precision : %.4f; recall: %.4f" % (marco_precision/N, marco_recall/N)



if __name__ == '__main__':
    evaluate_s(
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.s",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo",
        "/home/disk2/wangjianxiang01/BaiduIntern/SPO_url/test_data/org/org.test.data.filtered.spo.someP.pred",
    )