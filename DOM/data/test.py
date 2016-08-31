# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open("test.manualtag") as fin, open("test.manualtag.tsv", "w") as fout:

    fout.write("url\ts\tp\to\tgold_s\tgold_o\n")
    lines = [line.strip() for line in fin]
    for line in lines:
        if line.startswith("# ------------------"):
            url = ""
            continue

        if line.startswith("URL:"):
            url = line.replace("URL:", "")
        else:
            s, p, o = line.split("\t")
            fout.write("%s\t%s\t%s\t%s\t\t\n" % (url, s, p, o))


