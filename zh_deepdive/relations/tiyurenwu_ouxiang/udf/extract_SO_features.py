#! /usr/bin/env python
# coding: utf-8
from deepdive import *
import ddlib, sys
reload(sys)
sys.setdefaultencoding("utf-8")

@tsv_extractor
@returns(lambda
    S_id    = "text",
    O_id    = "text",
    feature = "text",
    : [])
def extract(
    S_id            = "text",
    O_id            = "text",
    S_begin_index   = "int",
    S_end_index     = "int",
    O_begin_index   = "int",
    O_end_index     = "int",
    sent_id         = "text",
    tokens          = "text[]",
    pos_tags        = "text[]",
    ner_tags        = "text[]",
    dep_types       = "text[]",
    dep_tokens      = "int[]"
):
    """
    Uses DDLIB to generate features for relation.
    """
    # Create a DDLIB sentence object, which is just a list of DDLIB Word objects
    sent = []
    if len(tokens) != len(pos_tags):
        print >>sys.stderr, '===>>>', sent_id, len(tokens), len(pos_tags)
    for i,t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=tokens[i],
            pos=pos_tags[i],
            ner=ner_tags[i],
            dep_par=dep_tokens[i] - 1,  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT
            dep_label=dep_types[i]))

    # Create DDLIB Spans for the two person mentions
    S_span = ddlib.Span(begin_word_id=S_begin_index, length=(S_begin_index-S_end_index+1))
    O_span = ddlib.Span(begin_word_id=O_begin_index, length=(O_begin_index-O_end_index+1))

    # Generate the generic features using DDLIB
    for feature in ddlib.get_generic_features_relation(sent, S_span, O_span):
        yield [S_id, O_id, feature]