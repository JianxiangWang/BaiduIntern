# coding: utf-8
import sys, json, codecs
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs
import glob
import json
import random


def sample_predict_with_confidence(model_dir, N, to_file):

    all_predicts = []

    for predict_file in glob.glob('%s/*/predict.json' % model_dir):

        dict_predict = json.load(open(predict_file))
        for P in dict_predict:
            all_predicts += [(s, P, o, str(prob)) for s, o, prob in dict_predict[P]]

    all_predicts = list(set(all_predicts))
    sampled = random.sample(all_predicts, N)
    sampled = sorted(sampled, key=lambda x: x[1])

    fout = codecs.open(to_file, "w", encoding="utf-8")
    fout.write("S,P,O,置信度\n")
    fout.write("\n".join([",".join(item) for item in sampled]))
    fout.close()


def sample_predict(model_dir, N, to_file):

    all_predicts = []

    for predict_file in glob.glob('%s/*/predict.json' % model_dir):

        dict_predict = json.load(open(predict_file))
        for P in dict_predict:
            all_predicts += [(s, P, o) for s, o, prob in dict_predict[P]]

    all_predicts = list(set(all_predicts))
    sampled = random.sample(all_predicts, N)
    sampled = sorted(sampled, key=lambda x: x[1])

    fout = codecs.open(to_file, "w", encoding="utf-8")
    fout.write("S,P,O\n")
    fout.write("\n".join([",".join(item) for item in sampled]))
    fout.close()


if __name__ == '__main__':
    sample_predict("models", 100, "predict_sample100.csv")
