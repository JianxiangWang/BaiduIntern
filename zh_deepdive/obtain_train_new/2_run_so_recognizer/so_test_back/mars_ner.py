#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
import glob
import os
import cPickle as pickle

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def train_pos_tagger():
    """
    Trains a POS tagger with sentences from Penn Treebank
    and returns it.
    """
    #train_sents = treebank.tagged_sents(simplify_tags=True)
    train_sents = treebank.tagged_sents(tagset='universal')
    tagger = nltk.TrigramTagger(train_sents, backoff=
        nltk.BigramTagger(train_sents, backoff=
        nltk.UnigramTagger(train_sents, backoff=
        nltk.DefaultTagger("NN"))))
    return tagger

def ce_phrases():
    """
    Returns a list of phrases found using bootstrap.py ordered
    by number of words descending (so code traversing the list
    will encounter the longest phrases first).
    """
    def by_phrase_len(x, y):
        lx = len(word_tokenize(x))
        ly = len(word_tokenize(y))
        if lx == ly:
            return 0
        elif lx < ly:
            return 1
        else:
            return -1
    ceps = []
    phrasefile = open("ce_phrases.txt", 'rb')
    for cep in phrasefile:
        ceps.append(cep[:-1])
    phrasefile.close()
    return map(lambda phrase: word_tokenize(phrase),
        sorted(ceps, cmp=by_phrase_len))

def ce_phrase_words(ce_phrases):
    """
    Returns a set of words in the ce_phrase list. This is
    used to tag words that refer to the NE but does not
    have a consistent pattern to match against.
    """
    ce_words = set()
    for ce_phrase_tokens in ce_phrases:
        for ce_word in ce_phrase_tokens:
            ce_words.add(ce_word)
    return ce_words

def slice_matches(a1, a2):
    """
    Returns True if the two arrays are content wise identical,
    False otherwise.
    """
    if len(a1) != len(a2):
        return False
    else:
        for i in range(0, len(a1)):
            if a1[i] != a2[i]:
                return False
        return True
    
def slots_available(matched_slots, start, end):
    """
    Returns True if all the slots in the matched_slots array slice
    [start:end] are False, ie, available, else returns False.
    """
    return len(filter(lambda slot: slot, matched_slots[start:end])) == 0

def promote_coreferences(tuple, ce_words):
    """
    Sets the io_tag to True if it is not set and if the word is
    in the set ce_words. Returns the updated tuple (word, pos, iotag)
    """
    return (tuple[0], tuple[1],
        True if tuple[2] == False and tuple[0] in ce_words else tuple[2])

def tag(sentence, pos_tagger, ce_phrases, ce_words):
    """
    Tokenizes the input sentence into words, computes the part of
    speech and the IO tag (for whether this word is "in" a CE named
    entity or not), and returns a list of (word, pos_tag, io_tag)
    tuples.
    """
    tokens = word_tokenize(sentence)
    # add POS tags using our trained POS Tagger
    pos_tagged = pos_tagger.tag(tokens)
    # add the IO(not B) tags from the phrases we discovered
    # during bootstrap.
    words = [w for (w, p) in pos_tagged]
    pos_tags = [p for (w, p) in pos_tagged]
    io_tags = map(lambda word: False, words)
    for ce_phrase in ce_phrases:
        start = 0
        while start < len(words):
            end = start + len(ce_phrase)
            if slots_available(io_tags, start, end) and \
                    slice_matches(words[start:end], ce_phrase):
                for j in range(start, end):
                    io_tags[j] = True
                start = end + 1
            else:
                start = start + 1
    # zip the three lists together
    pos_io_tagged = map(lambda ((word, pos_tag), io_tag):
        (word, pos_tag, io_tag), zip(zip(words, pos_tags), io_tags))
    # "coreference" handling. If a single word is found which is
    # contained in the set of words created by our phrases, set
    # the IO(not B) tag to True if it is False
    return map(lambda tuple: promote_coreferences(tuple, ce_words),
        pos_io_tagged)

shape_A = re.compile("[A-Zbdfhklt0-9#$&/@|]")
shape_x = re.compile("[acemnorsuvwxz]")
shape_i = re.compile("[i]")
shape_g = re.compile("[gpqy]")
shape_j = re.compile("[j]")

def shape(word):
    wbuf = []
    for c in word:
        wbuf.append("A" if re.match(shape_A, c) != None
            else "x" if re.match(shape_x, c) != None
            else "i" if re.match(shape_i, c) != None
            else "g" if re.match(shape_g, c) != None
            else "j")
    return "".join(wbuf)

def word_features(tagged_sent, wordpos):
    return {
        "word": tagged_sent[wordpos][0],
        "pos": tagged_sent[wordpos][1],
        "prevword": "<START>" if wordpos == 0 else tagged_sent[wordpos-1][0],
        "prevpos": "<START>" if wordpos == 0 else tagged_sent[wordpos-1][1],
        "nextword": "<END>" if wordpos == len(tagged_sent)-1
                                                else tagged_sent[wordpos+1][0],
        "nextpos": "<END>" if wordpos == len(tagged_sent)-1
                                             else tagged_sent[wordpos+1][1],
        "shape": shape(tagged_sent[wordpos][0])
    }

def train_ner(pickle_file):
    featuresets = []
    for line in sys.stdin:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        json_info = json.loads(field[0])
        tagged_sent = json_info['label']
        #print >> sys.stderr, json.dumps(tagged_sent, ensure_ascii = False)
        for idx, (word, pos_tag, io_tag) in enumerate(tagged_sent):
            featuresets.append((word_features(tagged_sent, idx), io_tag))
    split = int(0.9 * len(featuresets))
#    random.shuffle(featuresets)
    train_set, test_set = featuresets[0:split], featuresets[split:]
#    classifier = nltk.NaiveBayesClassifier.train(train_set)
#    classifier = nltk.DecisionTreeClassifier.train(train_set)
    classifier = nltk.MaxentClassifier.train(train_set, algorithm="GIS", trace=0)
    # evaluate classifier
    print "accuracy=", nltk.classify.accuracy(classifier, test_set)
    if pickle_file != None:
        # pickle classifier
        pickled_classifier = open(pickle_file, 'wb')
        pickle.dump(classifier, pickled_classifier)
        pickled_classifier.close()
    return classifier

def get_trained_ner(pickle_file):
    pickled_classifier = open(pickle_file, 'rb')
    classifier = pickle.load(pickled_classifier)
    pickled_classifier.close()
    return classifier

def test_ner(input_file, classifier):
    #pos_tagger = train_pos_tagger()
    #input = open(input_file, 'rb')
    for line in sys.stdin:
        line = line[:-1]
        if len(line.strip()) == 0:
            continue
        field = line.split('\t')
        json_info = json.loads(field[0])
        tagged_sent = json_info['label']
        io_tags = []
        for idx, (word, pos_tag, io_tag) in enumerate(tagged_sent):
            io_tags.append(classifier.classify(word_features(tagged_sent, idx)))
        ner_sent = zip(tagged_sent, io_tags)
        print_sent = []
        for token, io_tag in ner_sent:
            #print >> sys.stderr, json.dumps(token, ensure_ascii = False)
            if io_tag == True:
                print_sent.append("<u>" + token[0] + "</u>")
            else:
                print_sent.append(token[0])
        print " ".join(print_sent)

def test_line_ner(sent_tags, classifier):
    #pos_tagger = train_pos_tagger()
    #input = open(input_file, 'rb')
    #print >> sys.stderr, 'input is: %s' % json.dumps(sent_tags, ensure_ascii = False)
    ret_list = []
    if len(sent_tags) == 0:
        return ret_list
    io_tags = []
    for idx, (word, pos_tag, beg_pos, end_pos) in enumerate(sent_tags):
        io_tags.append(classifier.classify(word_features(sent_tags, idx)))
    ner_sent = zip(sent_tags, io_tags)
    print_sent = []
    index = 0
    while True:
        token, io_tag =  ner_sent[index]
        #print >> sys.stderr, index
        #print >> sys.stderr, len(ner_sent)
        #print >> sys.stderr, io_tag
        #print >> sys.stderr, json.dumps(token, ensure_ascii = False)
        if io_tag == True:
            new_chunk = token[0]
            index2 = -1
            end_pos = token[2] + len(token[0])
            if index + 1 < len(ner_sent):
                for index2, (new_token, new_io_tag) in enumerate(ner_sent[index+1:]):
                    if new_io_tag == True:
                        #new_chunk += '\x01' + new_token[0]
                        new_chunk += new_token[0]
                        end_pos = new_token[2] + len(new_token[0])
                    else:
                        break
            #print >>sys.stderr, json.dumps(ner_sent[index], ensure_ascii = False)
            #ret_list.append([new_chunk, ner_sent[index][0][2], end_pos - ner_sent[index][0][2]])
            ret_list.append([sentence[ner_sent[index][0][2]:end_pos], ner_sent[index][0][2], end_pos - ner_sent[index][0][2]])
            index += 2 + index2
        else:
            index += 1
        if index >= len(ner_sent):
            break
    return ret_list

class MarsNer:
    def __init__(self, model_file):
        self.classifier = get_trained_ner(model_file)
        self.name = model_file.split('/')[-1]
        return

    def predict(self, sentence_info):
        sent_tags = sentence_info['ner_result']
        sentence = sentence_info['sentence']
        ner_list = test_line_ner(sent_tags, self.classifier)
        #ret_list = filter(lambda x: sentence.find(x)!=-1, ner_list)
        ret_list = [ [x[0], self.name, x[1], x[2]] for x in ner_list ]
        return ret_list

class MarsNerAll:
    def __init__(self, model_dir):
        self.pattern = re.compile(ur'^(.*)\[([^\[]+)\]$')
        self.classifier_list = []
        for model_file in glob.glob(model_dir + '/*'):
            self.classifier_list.append(MarsNer(model_file))
        return

    def predict(self, sentence_info):
        ner_list = []
        for classifier in self.classifier_list:
            ner_list.extend(classifier.predict(sentence_info))
        return ner_list

def print_file( ):
    print __file__
    local_dir = os.path.dirname(__file__)
    local_file = os.path.basename(__file__)
    with open(local_dir + '/prop_2') as in_file:
        for line in in_file:
            print line
    return

def load_s_dict(s_file):
    ret_dict = {}
    with open(s_file) as in_file:
        for line in in_file:
            line = line.decode('utf-8').rstrip('\r\n')
            field = line.split('\t')
            domain_local = field[0]
            type_local = field[1].replace(u'，', u',').split(',')
            ret_dict[domain_local] = set(type_local)
    return ret_dict

def load_o_dict(o_file):
    ret_dict = {}
    with open(o_file) as in_file:
        for line in in_file:
            line = line.decode('utf-8').rstrip('\r\n')
            field = line.split('\t')
            domain_local = field[1]
            type_local = field[2]
            key = domain_local + u'_' + type_local
            des_type = field[3].replace(u'，', u',').split(',')
            ret_dict[key] = set(des_type)
    return ret_dict

def add_ner_result_index(sentence_info, sentence, pattern):
    """
    将ner结果中增加词的起始和终止index
    """
    ret_list = []
    beg_pos = 0
    if 'ner' in sentence_info:
        for item in sentence_info['ner']:
            match_object = re.search(pattern, item)
            if match_object:
                word = match_object.group(1)
                ner = match_object.group(2)
                if sentence.find(word, beg_pos) != -1:
                    beg_pos = sentence.find(word, beg_pos)
                    ret_list.append([word, ner, beg_pos, len(word)])
    return ret_list


def get_mars_ner_result(domain_predicate, s_prop, o_prop, ner_result, predict_result):
    """
    根据多个来源数据, 对模型结果做格式转换

    PARAMETERS:
    domain_predicate: [INPUT], 领域和p的列表
    s_prop: [INPUT], p对s的限制
    o_prop: [INPUT], p对o的限制
    ner_result: [INPUT], nlp_ner工具的返回结果
    predict_rsult: [INPUT], 我们模型的返回结果

    RETURNS:
    """
    ret_dict = {}
    #根据so识别结果和不同p对so的要求，转换格式
    for item in domain_predicate:
        ret_dict[item] = {}
        s_result = []
        domain, predicate = item.split('_')
        if domain in s_prop:
            for tag in ner_result:
                if tag[1] in s_prop[domain]:
                    s_result.append(tag)
        ret_dict[item]['s'] = s_result
        o_result = []
        if item in o_prop:
            for tag in ner_result:
                if tag[1] in o_prop[item]:
                    o_result.append(tag)
            for tag in predict_result:
                if tag[1] in o_prop[item]:
                    o_result.append(tag)
        ret_dict[item]['o'] = o_result
    return ret_dict

def main():
    classifier = MarsNerAll('models')
    s_prop = load_s_dict('s_prop')
    o_prop = load_o_dict('o_prop')

    pattern = re.compile(ur'^(.*)\[([^\[]+)\]$')
    for line in sys.stdin:
        line = line.decode('utf-8').rstrip('\r\n')
        field = line.split('\t')
        json_info = json.loads(field[0])
        sentence = json_info['sentence']
        json_info['ner_result'] = add_ner_result_index(json_info, sentence, pattern)
        #模型预测
        predict_result = classifier.predict(json_info)

        domain_predicate = json_info['domain']
        out_info = {}
        out_info['sentence'] = json_info['sentence']
        out_info['url'] = json_info['url']
        out_info['publishTime'] = json_info['publishTime']
        out_info['linkFoundTime'] = json_info['linkFoundTime']
        out_info['depparser'] = json_info['depparser']
        out_info['p_list'] = json_info['domain']
        ner_result = json_info['ner_result']
        #print >> sys.stderr, json.dumps(predict_result, ensure_ascii = False)
        out_info['mars_ner'] = get_mars_ner_result(domain_predicate, s_prop, o_prop, ner_result, predict_result)
        print json.dumps(out_info, ensure_ascii = False)
    return
    
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
