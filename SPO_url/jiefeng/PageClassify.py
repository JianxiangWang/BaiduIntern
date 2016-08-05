#-*-coding:utf8-*-
from __future__ import division
import sys
import json
from PageInfo import PageInfo

class PageClassify:
    pageinfo_type = ''
    
    def __init__(self, pageinfo_type='crawl_pack'):
        """prepared:输入为预先解析的页面信息，如页面类型，title，格式： url \t pageinfo(json)
           crawl_pack:需要抓取页面，返回和prepared相同格式 
        """
        if pageinfo_type == 'prepared':
            self.pageinfo_type = 'prepared'
        else:
            self.pageinfo_type = 'crawl_pack'
            self.page_info     = PageInfo()
        
    def get_pageinfo(self, input):
        page_str = ''
        if self.pageinfo_type == 'crawl_pack':
            url = input
            page_flag, page_str = self.page_info.get_pageinfo(url) # 判断库中是否有该url，获取页面类型
            if page_flag == -1:
                return -1, ''
            elif page_flag == -2:
                return -2, ''
            
        elif self.pageinfo_type == 'prepared':
            page_str = input
                
        info = page_str.strip().split('\t')
        url  = info[0]
        try:
            json_info = json.loads(info[1].decode('utf8', 'ignore'))
        except:
            return -2, ''
        # json_info : url, page_type, title, realtitle, content, cont_html, kv_dict, article
        page_info = self.trans_code(json_info)
        return 1, page_info
    
    def trans_code(self, json_info):
        page_info = {
            'url'       : json_info['url'].encode('utf8'),
            'page_type' : [],
            'title'     : json_info['title'].encode('utf8'),
            'realtitle' : json_info['realtitle'].encode('utf8'),
            'content'   : json_info['content'].encode('utf8'),
            'cont_html' : json_info['cont_html'].encode('utf8'),
            'kv_dict'   : {},
            'article'   : json_info['article'].encode('utf8')
        }
        for item in json_info['page_type']:
            page_info['page_type'].append(item.encode('utf8'))
        for item in json_info['kv_dict']:
            key = item.encode('utf8')
            value = []
            for v_item in json_info['kv_dict'][item]:
                value.append(v_item.encode('utf8'))
            page_info['kv_dict'][key] = value
        return page_info
    
    def classify_evaluating(self, input):
        """评测"""
        page_flag, page_info = self.get_pageinfo(input)
        
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''
        
        page_info['domain'] = '评测'
        
        if '文章内容页' not in page_info['page_type'] and '商品详情页' not in page_info['page_type']:
            return 0, ''

        if page_info['realtitle'].find('测评') != -1 or page_info['realtitle'].find('评测') != -1:
            return 1, page_info

        valid_count = 0
        key_words   = ['评测', '测评', '参数', '做工', '设计', '性价比', '优点', '缺点']
        for item in key_words:
            if page_info['content'].find(item) != -1:
                valid_count += 1
        if valid_count >= 4:
            return 1, page_info
        else:
            return 0, ''
        
    def classify_introduction(self, input):
        """简介"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:      
            return -1, ''
        elif page_flag == -2:
            return -2, ''
        
        page_info['domain'] = '简介'
        baike_res, baike_title = self.classify_baike(input)
        if '文章内容页' not in page_info['page_type'] and baike_res==0 and page_info['url'].find('zhidao.baidu.com')==-1:
            return 0, ''

        title_count = 0
        cont_count  = 0

        title_words = ['简介', '介绍']
        for item in title_words:
            if page_info['realtitle'].find(item) != -1:
                title_count += 1

        cont_words = ['简介', '介绍', '剧情']
        for item in cont_words:
            if page_info['content'].find(item) != -1:
                cont_count += 1

        valid_count = title_count*1 + cont_count*1
        if valid_count >= 1:
            return 1, page_info
        else:
            return 0, ''
        
    def classify_news(self, input):
        """新闻"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''
        
        page_info['domain'] = '新闻'
        if '新闻内容页' in page_info['page_type']:
            return 1, page_info
        else:
            return 0, ''

    def classify_personalprofile(self, input):
        """个人资料"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''
        
        page_info['domain'] = '个人资料'
        kv_count    = 0
        cont_count  = 0
        if page_info['realtitle'].find('个人资料') != -1:
            return 1, page_info

        kv_words = ['姓名', '生日', '出生日期', '出生地', '民族', '身高', '体重', '爱好', '职业']
        for item in kv_words:
            if item in page_info['kv_dict']:
                kv_count += 1
                            
        cont_words = ['个人经历', '个人简介', '个人资料', '主要作品', '基本信息', '人物评价']
        for item in cont_words:
            if page_info['content'].find(item) != -1:
                cont_count += 1
                                            
        valid_count = kv_count*1 + cont_count*2
        if valid_count >= 4:
            return 1, page_info
        else:
            return 0, ''

    def classify_baike(self, input):
        """百科"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''

        page_info['domain'] = '百科'
        if page_info['url'][:7] == 'http://':
            url = page_info['url'][7:]
        else:
            url = page_info['url']
            
        main_site = url.split('/')[0]
        if main_site == 'baike.sogou.com':
            if url[16] == 'v':
                return 1, page_info
            else:
                return 0, ''
        else:
            valid_set = (
                'baike.baidu.com/item',
                'baike.baidu.com/view',
                'baike.baidu.com/subview',
                'wapbaike.baidu.com/item',
                'wapbaike.baidu.com/view',
                'wapbaike.baidu.com/subview',
                'm.baike.so.com/doc',
                'baike.so.com/doc',
                'www.baike.com/wiki'
            )
            url_subdomain = '/'.join(url.split('/')[:2])
            if url_subdomain in valid_set:
                return 1, page_info
            else:
                return 0, ''

    def classify_weibo(self, input):
        """微博"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''
        
        page_info['domain'] = '微博'
        if page_info['url'][:7] == 'http://':
            url = page_info['url'][7:]
        else:
            url = page_info['url']
            
        main_site = url.split('/')[0]
        if main_site == 'weibo.com':
            if url[9:12] == '/u/':
                return 1, page_info
            domains = url.split('/')
            if len(domains) == 2:
                return 1, page_info
            else:
                return 0, ''
        elif main_site == 'www.weibo.com':
            if url[9:12] == '/u/':
                return 1, page_info
            elif url[9:12] == '/p/':
                tag = url.split('?')[0].split('/')[-1]
                if tag == 'home':
                    return 1, page_info
                else:
                    return 0, ''
            domains = url.split('/')
            if len(domains) == 2:
                return 1, page_info
            else:
                return 0, ''
        elif main_site == 't.qq.com':
            if url[8:13] == '/p/t/':
                return 0, ''
            domains = url.split('/')
            if len(domains) == 2:
                return 1, page_info
            else:
                return 0, ''
        else:
            return 0, ''
        
    def classify_commidity(self, input):
        """商品"""
        page_flag, page_info = self.get_pageinfo(input)
        if page_flag == -1:
            return -1, ''
        elif page_flag == -2:
            return -2, ''

        page_info['domain'] = '商品'
        if '商品详情页' in page_info['page_type']:
            return 1, page_info
        else:
            return 0, ''
        
    def test_precision_recall(self, test_dict):
        """准招计算"""
        func_dict = {
            'baike'  : self.classify_baike,
            'weibo'  : self.classify_weibo,
            'news'   : self.classify_news,
            'ceping' : self.classify_evaluating,
            'goods'  : self.classify_commidity,
            'personinfo' : self.classify_personalprofile,
            'abstract'   : self.classify_introduction
        }

        for domain in test_dict:
            print '# ' + domain + ' ---------'

            precision = ''
            recall    = ''

            def get_pr(pr):
                total = 0
                valid = 0

                for item in test_dict[domain][pr]:
                    url = item['url']
                    tag = item['tag']
                    func = func_dict[domain]
                    pre, page_info = func(url)
                    print pr + '\t' + url + '\t' + str(tag) + '\t' + str(pre)
                    if pre == -1 or pre == -2:
                        continue
                    total += 1
                    if pre == tag:
                        valid += 1
                if total == 0:
                    return '0%'
                return str(round((valid/total),4)*100) + '%'

            precision = get_pr('precision')
            recall    = get_pr('recall')
            print 'precision : ' + precision
            print 'recall : ' + recall
        
    def predict(self, input):
        """页面类型预测"""
        def print_res(func):
            res, page_info = func
            if res == 1:
                print_str = page_info['url'] + '\t' + page_info['realtitle'] + '\t' + page_info['domain'] + '\t' + page_info['url']
                print print_str
                
        print_res(self.classify_evaluating(input))
        print_res(self.classify_introduction(input))
        print_res(self.classify_news(input))
        print_res(self.classify_personalprofile(input))
        print_res(self.classify_baike(input))
        print_res(self.classify_weibo(input))
        print_res(self.classify_commidity(input))
        
        
