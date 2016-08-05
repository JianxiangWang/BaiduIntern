import sys
import os
import json
import ConfigParser
import hashlib

class PageInfo:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        path   = '../paramaters.conf'
        config.read(path)
        self.wdbtools_path = config.get('path', 'wdbtools')
        self.work_dir      = config.get('path', 'work_dir')
        self.data_path     = self.work_dir + config.get('path', 'data_dir')
        self.tools_path    = self.work_dir + config.get('path', 'tools_dir')
    
        if not os.path.exists(self.wdbtools_path + 'seekone' ):
            print 'wdbtools not found.'
        if not os.path.exists(self.work_dir):
            print 'word dir set wrong.'

    def get_pageinfo(self, url):
        url_md5   = hashlib.md5(url).hexdigest()  
        data_path = self.data_path + url_md5
        if os.path.exists(data_path):
            page_str = open(data_path).read().strip()
            return 1, page_str
        
        pack_exist = self.get_pack(url)
        if pack_exist == 0:
            return -1, ''

        str_exist, page_str = self.get_pagestr(url)
        if str_exist == 1:
            return 1, page_str
        else:
            return -2, ''

    def get_pack(self, url):
        url_md5   = hashlib.md5(url).hexdigest()
        pack_path = self.data_path + 'pack/' + url_md5

        if not os.path.exists(pack_path):
            cmd_seekone = self.wdbtools_path + 'seekone "' + url + '" PAGE > ' + pack_path +'.tmp 2>/dev/null'
            os.system(cmd_seekone)
            os.system('sed -e \'1,2d\' ' + pack_path + '.tmp >' + pack_path + ' && rm ' + pack_path + '.tmp')
        
        pack_info = open(pack_path).read()
        if pack_info.find('ACK : FAIL') != -1:
            return 0
        else:
            return 1

    def get_pagestr(self, url):
        url_md5   = hashlib.md5(url).hexdigest()
        pack_path = self.data_path + 'pack/' + url_md5
        data_path = self.data_path + url_md5
        pt_path   = data_path + '.pt'
        page_path = data_path + '.page'
        cmd_pt   = 'cd ' + self.tools_path + ' && cat ' + pack_path + ' | python get_ptnumber.py > ' + pt_path
        cmd_page = 'cd ' + self.tools_path + 'page_extract && cat ' + pack_path + ' | ./data_extract | python ../get_pageextract.py > ' + page_path + ' 2>/dev/null'
        cmd_data = 'cd ' + self.tools_path + 'varemark && cat ' + pack_path + ' | ./test_vareamark -t central -o 2 | python ../get_varemark.py | python ../get_all.py '+ page_path +' '+ pt_path +' > ' + data_path + ' 2>/dev/null'
        cmd_clean = 'rm ' + pt_path + ' && rm ' + page_path
        
        pt_res = os.system(cmd_pt)
        if pt_res != 0:
            return 0, ''
        
        page_res = os.system(cmd_page)
        if page_res != 0:
            return 0, ''
        
        data_res = os.system(cmd_data)
        if data_res != 0:
            os.system('rm ' + data_path)
            return 0, ''
        
        os.system(cmd_clean)
        try:
            page_str = open(data_path).read().strip()
            return 1, page_str
        except:
            return 0, ''
        

