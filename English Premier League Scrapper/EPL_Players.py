import scrapy
#from scrapy.utils.response import open_in_browser
import json

base= 'https://footballapi.pulselive.com/football/players?pageSize=30&compSeasons={}&altIds=true&page={}&type=player&id=-1&compSeasonId={}'
#global season 
seasons_list=['418','363','274','210','79','54','42','27','22','21','20','19','18']
#season=418

def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d
    
    
h=get_headers(''' 
                  Host: footballapi.pulselive.com
                  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0
                  Accept: */*
                  Accept-Language: en-US,en;q=0.5
                  Accept-Encoding: gzip, deflate, br
                  Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                  Origin: https://www.premierleague.com
                  Connection: keep-alive
                  Referer: https://www.premierleague.com/
                  Sec-Fetch-Dest: empty
                  Sec-Fetch-Mode: cors
                  Sec-Fetch-Site: cross-site
                  DNT: 1
                  Sec-GPC: 1
                  Pragma: no-cache
                  Cache-Control: no-cache ''')


class EplPlayersSpider(scrapy.Spider):
    name = 'EPL_Players'    
    #start_urls = [base.format(0)]    
    
    def __init__(self, *args, **kwargs):  
      self.num_s=0
    
    
    def start_requests(self):       
       #for season in seasons_list: 
           
           req=scrapy.Request(base.format(418,0,418),headers=h)
           yield req
    

    def parse(self, response):
        #for season in seasons_list:  
        #open_in_browser(response)
                #print (response.meta.get('index'))
                
                raw_data=response.body
                data=json.loads(raw_data)                                       
                if data['content']:
                    yield data
                #print ('SEASON:',season)             
                #Max_Pages= (data['pageInfo']['numPages'])
                    Current_Page=(data['pageInfo']['page'])
                    next_page_url=base.format(seasons_list[self.num_s],Current_Page+1,seasons_list[self.num_s])
                    #next_page_url=base.format(seasons_list[n],Current_Page+1,seasons_list[n])
                    yield scrapy.Request(next_page_url,headers=h, callback=self.parse)
                else:     
                    if self.num_s < len(seasons_list):
                        self.num_s+=1
                        next_season_url=base.format(seasons_list[self.num_s],0,seasons_list[self.num_s])
                        yield scrapy.Request(next_season_url,headers=h, callback=self.parse)
