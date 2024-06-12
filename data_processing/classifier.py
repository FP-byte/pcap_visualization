from collections import Counter
import re
from collections import defaultdict
from pcap_analysis.basic import BaseDataObject
import pandas as pd

class Classifier(BaseDataObject):

    keywords = ['google', 'youtube', 'twitter', "instagram", "weibo", 'adobe', "360cnd", 'amazon', "github", "blogspot", "pinterest", 'apple', "tumbler" "t.co", "x.com", "alibaba|alicdn|alipay", "twitch", "wikipedia", "reddit", "baidu", "yahoo", "facebook", "mail.ru", "taobao", "tmaill", "twimg", "vk", "aliexpress", "amazon", "reddit", "tiktok", "bing", "msn", "netfilix", "ebay", "yandex", "imgur", "github", "blogger" "linkedin", "live.com"]
    

    categories = {
            'social media':['twitter', "instagram", "pinterest",  "tumbler" "t.co", "x.com", 'facebook', "vk", "weibo", 'reddit', 'imgur'],
            'google': ['google', 'gstatic', 'doubleclick'],
            'yahoo' : ['yahoo', 'yahoocnd'],
            'apple' : ['apple'],
            "amazon" : ['amazon'],
            'other seach engines': ['baidu', 'yandex', 'brave'],
            'microsoft': ["bing", "msn", "live.com", 'microsoft', 'aws'],
            'email': ['mail.ru', 'mail'],
            'streaming': ['youtube', 'netflix', 'hbo', 'videoland'],
            'shopping': ["360cnd", 'ali', 'alibaba', 'aliexpress', 'alipay', 'alicnd'],
            'selling': ["ebay", 'marktplaats'],
            'development': ['github', 'stackoverflow'],
            'plugins': ['ublockorigin', '.dev'],
            'blogging': ['wordpress', 'blogspot']

        }
    
    def infer_keywords_from_domains(sef):
        pass