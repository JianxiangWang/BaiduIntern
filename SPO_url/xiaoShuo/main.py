#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import sys, hashlib
import os

# # 输入url, 判断是不是 小说
# def main(urls_file, predict_file):
#
#     fout = open(predict_file, "w")
#     for line in open(urls_file):
#
#         url = line.strip()
#         if is_xiaoShuo(url):
#             title = get_url_title(url)
#             S = title
#             P = "体裁/小说"
#             O = url
#
#             fout.write("%s\t%s\t%s\n" % (S, P, O))
#
#             print "==> %s: %s\t%s" % (url, S, P)
#         else:
#             print "==> %s: %s\t%s" % (url, "", "")
#
#     fout.close()

# 输入url, 判断是不是 小说
def main():

    for line in sys.stdin:
        url = line.strip()
        if is_xiaoShuo(url):
            title = get_url_title(url)
            S = title
            P = "体裁/小说"
            O = url

            print "%s\t%s\t%s\t%s" % (url, S, P, O)


def is_xiaoShuo(url):

    cmd = "../tools/run_wdbtools-pc.sh %s" % (url)
    # result = subprocess.check_output(cmd, shell=True)
    fin = os.popen(cmd)
    result = fin.readlines()[-1]

    page_type_list = eval(result.strip())
    if {"小说首页", "小说列表页"} & set(page_type_list):
        return True
    else:
        return False

def get_url_title(url):

    pack_file_path = _get_pack_file_path(url)
    # 根据pack,获取对应的title
    title = get_title_by_pack_file(pack_file_path)

    return title



def _get_pack_file_path(url):
    m = hashlib.md5()
    m.update(url)
    file_name = m.hexdigest()

    pack_file_path = os.getcwd() + "/packs/%s" % (file_name)
    if os.path.exists(pack_file_path):
        return pack_file_path
    else:
        # 抓url对应的pack
        wdbtools_path = "/home/disk2/wangjianxiang01/tools/wdbtools/output/client/bin"
        #  抓包 !
        cwd = "%s/seekone %s PAGE > %s " % (wdbtools_path, url, pack_file_path)
        os.system(cwd)
        #  删除前2行
        cwd = "sed '1, 2d' %s > tmp.txt && mv tmp.txt %s" % (pack_file_path, pack_file_path)
        os.system(cwd)
        return pack_file_path


def get_title_by_pack_file(pack_file):
    # cat pack.test.input | /test_vareamark -t realtitle -o 0 | iconv -f gb18030 -t utf-8
    varemark_path = "/home/disk2/wangjianxiang01/tools/varemark"

    cmd = "cd %s && cat %s | ./test_vareamark -t realtitle -o 0 | iconv -f gb18030 -t utf-8" % (varemark_path, pack_file)
    print cmd
    fin = os.popen(cmd)
    result = fin.readlines()

    if result == []:
        return "NULL"

    title = result[-1].strip().split(" | ")[-1]

    return title



if __name__ == '__main__':
    main()
