from collections import Counter
import re
from collections import defaultdict
from basic import BaseDataObject
import pandas as pd

class DataProcessor(BaseDataObject):
    """
    Process data for visualizations
    """
    
    clusters :list
    activity:pd.DataFrame
    urls_counts:pd.DataFrame

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

    def __init__(self, df_data: pd.DataFrame, df_urls:pd.DataFrame) -> None:
        self.df_data = df_data
        self.urls = df_urls
       # print('dataprocessing', datacleaner.df_data.columns)
        self.keywords = ['google', 'youtube', 'twitter', "instagram", "weibo", 'adobe', "360cnd", 'amazon', "github", "blogspot", "pinterest", 'apple', "tumbler" "t.co", "x.com", "alibaba|alicdn|alipay", "twitch", "wikipedia", "reddit", "baidu", "yahoo", "facebook", "mail.ru", "taobao", "tmaill", "twimg", "vk", "aliexpress", "amazon", "reddit", "tiktok", "bing", "msn", "netfilix", "ebay", "yandex", "imgur", "github", "blogger" "linkedin", "live.com"]
        self.count_urls()
        self.reg_patterns = {}
        self.clusters = {}
        self.df_urls_categorie = pd.DataFrame()
        self.labeled_clusters = {}
      

    def get_activity_df(self, url, time):
        visits = {}
        if url not in self.df_data['url']:
                visits[url] = {'start': time, 'end': time, 'duration': 0, 'count': 1}
        else:
                visits[url]['end'] = time
                visits[url].update({'duration': time - self.visits[url]['start']})
                visits[url]['count'] +=1
        self.activity = pd.DataFrame.from_dict(visits, orient="columns").T.reset_index()
        self.activity.columns=['url', 'start', 'end', 'duration', 'count']

    def get_cluster_names(self):
        if self.clusters:
            return list(self.clusters.keys())
        else:
            self.create_dns_clusters()
            return self.get_cluster_names()
                   
    def get_cluster_sizes(self):
        if self.clusters:
            return [len(self.clusters[name]) for name in self.cluster_names]
        else:
            self.create_dns_clusters()
            return self.get_cluster_sizes()

    def count_urls(self) -> pd.DataFrame :
        counts = Counter(self.urls)        
        urls_counts = pd.DataFrame.from_dict(counts, orient="index", columns=['count']).reset_index()
        
        #rename cols
        urls_counts.columns=['url', 'count']
        #sort values by count
        urls_counts.sort_values(by='count', inplace=True, ascending=False, ignore_index=True)
        #print(urls_counts)
        self.urls_counts = urls_counts

        return urls_counts

    def create_reg_patters(self):   
        reg_patterns = {}
        # Define regular expression patterns
        for k in self.keywords:
            s = re.compile(f"([a-z0-9-]+\.)*{k}([a-z0-9-]+\.)*")
            reg_patterns[k] = s
        reg_patterns["other"] = re.compile(".*")
        self.reg_patterns = reg_patterns

    def label_clusters(self):
        labeled_clusters = {}
        for name, urls in self.clusters.items():
            for category, keywords in self.categories.items():
                if name in keywords:
                      labeled_clusters[category] = {name : urls}

        
    def create_dns_clusters(self):
        self.create_reg_patters()
        # Initialize clusters
        clusters = defaultdict(list)
        
        # Match URLs to patterns and cluster them
        for url in self.urls_counts['url']:
            matched = False
            for name, pattern in self.reg_patterns.items():
                if pattern.match(url):
                    clusters[name].append(url)
                    matched = True
                    break
            if not matched:
                clusters["other"].append(url)

        self.clusters = clusters
    
    def print_clusers(self) -> str: 
        # Print clusters      
        for name, cluster in self.clusters.items():            
            print(f"{name}:")
            for url in cluster:
                print(f"  - {url}")

    def keyword_to_regex(self, keyword):
        return  f"([a-z0-9-]+\.)*{keyword}([a-z0-9-]+\.)*"
    
    def filter_urls_on_regexpattern(self, regex_pattern, df, bool=True):  
        # filter urls on the base of a regex pattern
            return  df[df['url'].str.contains(regex_pattern, na=False, regex=True) == bool]

            
    
    def create_regex_patters(self, keywords):
        keywords_regex_list = [f"([a-z0-9-]+\.)*{keyword}([a-z0-9-]+\.)*" for keyword in keywords]
        
        keywords_regex_joined = "|".join(keywords_regex_list)
        return  keywords_regex_list, keywords_regex_joined



    def add_lable_to_cluster(self):
        urls_overig = self.urls_counts.copy()
        dict_urls = {}
        for categorie, keywords in self.categories.items():
            df = {}
            # create a regex expression for each keyword
            keywords_regex_list, keywords_regex_joined = self.create_regex_patters(keywords)
            for keyword, regex in zip(keywords, keywords_regex_list):
                    selected_urls = self.filter_urls_on_regexpattern(re.compile(regex), urls_overig)
                    print(selected_urls)
                    if selected_urls.empty:
                        continue
                    df[keyword] = selected_urls
                    dict_urls[categorie] = df
            #filter out all urls with keywords
            urls_overig = self.filter_urls_on_regexpattern(keywords_regex_joined, urls_overig, False)
        self.labeled_clusters = dict_urls
        return dict_urls  
