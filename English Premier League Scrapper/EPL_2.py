import scrapy
import json

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


players = open('EPL_ids.json')
players_data = json.load(players)
ID_list = []
Name_list=[]

for i, player in enumerate(players_data):
      for j, player2 in enumerate(player['content']):    
              ID_website= (player2 ['id'])
              if ID_website not in ID_list:
                  ID_list.append(ID_website)
                  Name_list.append(player2['name']['display'])


class Epl2PySpider(scrapy.Spider):    
    name = 'EPL_2' 
    
    # custom_settings = {
    #     'CONCURRENT_REQUESTS' : 1
    #                                     }
       
    
    def start_requests(self):   
        for num,id in enumerate(ID_list):                                  
                #self.ID=ID_website
                req=scrapy.Request('https://www.premierleague.com/players/{}/{}/overview'.format(int(id),Name_list[num].replace(' ','-')),callback=self.parse1,meta={'index':id})
                #req=scrapy.Request('https://footballapi.pulselive.com/football/stats/player/{}?comps=1'.format(int(ID_website)),headers=h,callback=self.parse2)
                #req=scrapy.Request('https://www.premierleague.com/players/48285/Aaron-Ramsey/overview')
                yield req
 
    
    def parse1(self, response):
        
        Appearences=[]
        Appearnces_subs=[]
        Goals=[]
        Date_of_Birth=[]
        Player_of_the_Month_seasons=[]
        
        player_id=int(response.meta['index'])
        
        try:
            All_Clubs= response.xpath('//td[@class="team"]/a/span[@class="long"]/text()').getall()
        except:
            All_Clubs='no data'
        try:
            Club_Seasons= response.xpath('//td[@class="season"]/p/text()').getall()     
        except:
            Club_Seasons='no data'
        try:
            Appearnces_old= response.xpath('//td[@class="appearances"]/text()').getall()
            for appearence in Appearnces_old:
                if appearence.strip():
                    Appearences.append(appearence.strip())       
        except:
            Appearences='no data'      
        try:
            Appearnces_subs_old= response.xpath('//td[@class="appearances"]/span/text()').getall()
            for appearence2 in Appearnces_subs_old:
                if appearence2.strip():
                    Appearnces_subs.append(appearence2.strip(' ()'))
        except:
            Appearnces_subs='no data'
        try:
            Goals_old= response.xpath('//td[@class="goals"]/text()').getall()    
            for goal in Goals_old:
                if goal.strip():
                    Goals.append(goal.strip())
        except:
            Goals='no data'
        try:
            Nationality= response.xpath('//div/span[@class="playerCountry"]/text()').getall()
        except:
            Nationality='no data'               
        try:
            Date_of_Birth_old= response.xpath('//ul[@class="pdcol2"]/li/div[@class="info"]/text()').getall()
            for date in Date_of_Birth_old:
                if date.strip():
                    Date_of_Birth.append(date.strip())
        except:
            Date_of_Birth='no data'       
        try:
            Height= response.xpath('//ul[@class="pdcol3"]/li/div[@class="info"]/text()').getall()[0]
        except:
            Height='no data'
        try:
            weight= response.xpath('//ul[@class="pdcol3"]/li/div[@class="info"]/text()').getall()[1]
        except:
            weight='no data'
        try:
            Golden_Boot=response.xpath('//th[text()="Golden Boot"]/following-sibling::th[1]/text()').get()
        except:
            Golden_Boot='no data'
        try:
            Golden_Boot_seasons=response.xpath('//th[text()="Golden Boot"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Golden_Boot_seasons = list(dict.fromkeys(Golden_Boot_seasons))
        except:
            Golden_Boot_seasons='no data'
        try:             
            Player_of_the_Season=response.xpath('//th[text()="Player of the Season"]/following-sibling::th[1]/text()').get()
        except:
            Player_of_the_Season='no data'
        try:   
            Player_of_the_Season_seasons=response.xpath('//th[text()="Player of the Season"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Player_of_the_Season_seasons = list(dict.fromkeys(Player_of_the_Season_seasons))
        except:
              Player_of_the_Season_seasons='no data'     
        try:   
            Goal_of_the_Month=response.xpath('//th[text()="Goal of the Month"]/following-sibling::th[1]/text()').get()
        except:
              Goal_of_the_Month='no data' 
        try:  
            Goal_of_the_Month_seasons=response.xpath('//th[text()="Goal of the Month"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Goal_of_the_Month_seasons = list(dict.fromkeys(Goal_of_the_Month_seasons))
        except:
              Goal_of_the_Month_seasons='no data' 
        try:
            Premier_League_Champion=response.xpath('//th[text()="Premier League Champion"]/following-sibling::th[1]/text()').get()
        except:
              Premier_League_Champion='no data' 
        try:
            Premier_League_Champion_seasons=response.xpath('//th[text()="Premier League Champion"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Premier_League_Champion_seasons = list(dict.fromkeys(Premier_League_Champion_seasons))
        except:
              Premier_League_Champion_seasons='no data' 
        try:
            Playmaker=response.xpath('//th[text()="Playmaker"]/following-sibling::th[1]/text()').get()
        except:
              Playmaker='no data' 
        try:
            Playmaker_seasons=response.xpath('//th[text()="Playmaker"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Playmaker_seasons = list(dict.fromkeys(Playmaker_seasons))
        except:
              Playmaker_seasons='no data' 
        try:
            Player_of_the_Month=response.xpath('//th[text()="Player of the Month"]/following-sibling::th[1]/text()').get()
        except:
              Player_of_the_Month='no data' 
        try:
            Player_of_the_Month_seasons_old=response.xpath('//th[text()="Player of the Month"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Player_of_the_Month_seasons_old = list(dict.fromkeys(Player_of_the_Month_seasons_old))
            for trophy in Player_of_the_Month_seasons_old:
                Player_of_the_Month_seasons.append(trophy.replace(' ','').replace('\n',' '))
        except:
              Player_of_the_Month_seasons='no data' 
        try:
            Goal_of_the_Season=response.xpath('//th[text()="Goal of the Season"]/following-sibling::th[1]/text()').get()
        except:
              Goal_of_the_Season='no data' 
        try:
            Goal_of_the_Season_seasons=response.xpath('//th[text()="Goal of the Season"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Goal_of_the_Season_seasons = list(dict.fromkeys(Goal_of_the_Season_seasons))
        except:
              Goal_of_the_Season_seasons='no data' 
        try:
            Golden_Glove=response.xpath('//th[text()="Golden Glove"]/following-sibling::th[1]/text()').get()
        except:
              Golden_Glove='no data' 
        try:
            Golden_Glove_seasons=response.xpath('//th[text()="Golden Glove"]/parent::tr/following-sibling::tr[1]/td/table/tbody/tr/td/text()').getall()
            Golden_Glove_seasons = list(dict.fromkeys(Golden_Glove_seasons))
        except:
              Golden_Glove_seasons='no data' 

        req2=scrapy.Request('https://footballapi.pulselive.com/football/stats/player/{}?comps=1'.format(int(response.meta['index'])),headers=h,callback=self.parse2,meta={'index':player_id})
        
        dic1={
              
            'player_id': player_id,
            'clubs_played_for': All_Clubs,
            'clubs_played_for_by_season': Club_Seasons,
            'apperances_total': Appearences,
            'apperances_as_a_sub': Appearnces_subs,
            'goals_scored': Goals,
            'nationality': Nationality,
            'date_of_bith': Date_of_Birth,
            'height': Height,
            'weight': weight,
            'golden_boots_won': Golden_Boot,
            'golden_boots_won_by_season': Golden_Boot_seasons,
            'player_of_the_season_won': Player_of_the_Season,
            'player_of_the_season_won_by_season': Player_of_the_Season_seasons,
            'goal_of_the_month_won': Goal_of_the_Month,
            'goal_of_the_month_won_by_season': Goal_of_the_Month_seasons,
            'premier_league_champion': Premier_League_Champion,
            'premier_league_champion_by_season': Premier_League_Champion_seasons,
            'playmaker_won': Playmaker,
            'playmaker_won_by_season': Playmaker_seasons,
            'player_of_the_month_won': Player_of_the_Month,
            'player_of_the_month_won_by_season': Player_of_the_Month_seasons  , 
            'goal_of_the_season_won': Goal_of_the_Season,
            'goal_of_the_season_won_by_season': Goal_of_the_Season_seasons,
            'golden_glove_won': Golden_Glove,
            'golden_glove_won_by_season': Golden_Glove_seasons                                 
            }
        
        yield dic1
        yield req2
        
    
    def parse2(self, response):  
      
        goals='no data'  
        goals_per_match='no data'  
        headed_goals='no data'  
        goals_with_right_foot='no data'  
        goals_with_left_foot='no data'  
        penalties_scored='no data'  
        freekicks_scored='no data'  
        shots='no data'  
        shots_on_target='no data'  
        shooting_accuracy='no data'  
        hit_woodwork='no data'  
        big_chances_missed='no data'  
          
        assists='no data'  
        passes='no data'  
        passes_per_match='no data'  
        pass_accuracy='no data'  
        big_chances_created='no data'  
        crosses='no data'  
        cross_accuracy='no data'  
        accurate_long_balls='no data'  
        through_balls='no data'  
          
        yellow_cards='no data'  
        red_cards='no data'  
        fouls='no data'  
        offsides='no data'  
          
        tackles='no data'  
        tackle_success='no data'  
        blocked_shots='no data'  
        interceptions='no data'  
        total_clearances='no data'  
        head_clearnces='no data'  
        clean_sheets='no data'  
        goals_conceded='no data'    
        errors_leading_to_goal='no data'    
        own_goals='no data'    
        clearances_off_line='no data'  
        last_man_tackles='no data'  
        recoveries='no data'  
        duels_won='no data'  
        duels_lost='no data'  
        successful_50_50s='no data'  
        aerial_battles_won='no data'  
        aerial_battles_lost='no data' 
      
        saves='no data' 
        penalty_saves='no data' 
        punches='no data' 
        good_high_claim='no data' 
        sweeper_clearences='no data' 
        throw_outs='no data' 
        goal_kicks='no data' 
        catches='no data'  
      
        raw_data=response.body
        data=json.loads(raw_data)
        
        player_id=response.meta['index']
        name = (data['entity']['name']['display'])
        try: 
            position = (data['entity']['info']['position'])        
        except:
            position ='no data'
        try:           
            shirt_num=(data['entity']['info']['shirtNum'])
        except:
            shirt_num='no data'
        try:
            position_details=(data['entity']['info']['positionInfo'])
        except:
            position_details='no data'
        
        if (len(data['stats']))==0:
          pass          
        
        else:
          
          for stat in data['stats']:                 
            if stat['name']=='appearances':
                    appearences=stat['value']
            if stat['name']=='Goals' or stat['name']=='goals':
                    goals=stat['value']
            if stat['name']=='att_hd_goal':
                    headed_goals=stat['value']
            if stat['name']=='att_rf_goal':
                     goals_with_right_foot=stat['value']
            if stat['name']=='att_lf_goal':
                     goals_with_left_foot=stat['value']
            if stat['name']=='att_pen_goal':
                     penalties_scored=stat['value']
            if stat['name']=='att_freekick_goal':
                     freekicks_scored=stat['value']
            if stat['name']=='total_scoring_att':
                    shots=stat['value']
            if stat['name']=='ontarget_scoring_att':
                    shots_on_target=stat['value']
            if stat['name']=='hit_woodwork':
                    hit_woodwork=stat['value']
            if stat['name']=='big_chance_missed':
                    big_chances_missed=stat['value']
            if stat['name']=='goal_assist':
                    assists=stat['value']
            if stat['name']=='total_pass':
                    passes=stat['value']
            if stat['name']=='big_chance_created':
                    big_chances_created=stat['value']
            if stat['name']=='total_cross':
                    crosses=stat['value']
            if stat['name']=='yellow_card':
                    yellow_cards=stat['value']
            if stat['name']=='red_card':
                    red_cards=stat['value']
            if stat['name']=='fouls':
                    fouls=stat['value']
            if stat['name']=='total_offside':
                    offsides=stat['value']
            if stat['name']=='total_tackle':
                    tackles=stat['value']
            if stat['name']=='blocked_scoring_att':
                    blocked_shots=stat['value']
            if stat['name']=='interception':
                    interceptions=stat['value']
            if stat['name']=='total_clearance':
                    total_clearances=stat['value']
            if stat['name']=='effective_head_clearance':
                    head_clearnces=stat['value'] 
            if stat['name']=='clean_sheet':
                    clean_sheets=stat['value']
            if stat['name']=='saves':
                    saves=stat['value']
            if stat['name']=='penalty_save':
                    penalty_saves=stat['value']
            if stat['name']=='punches':
                    punches=stat['value']
            if stat['name']=='good_high_claim':
                    good_high_claim=stat['value']
            if stat['name']=='stand_catch':
                    catches_stand=stat['value']
            if stat['name']=='dive_catch':
                    catches_dive=stat['value']
            if stat['name']=='total_keeper_sweeper':
                    sweeper_clearences=stat['value']
            if stat['name']=='keeper_throws':
                    throw_outs=stat['value']
            if stat['name']=='goal_kicks':
                    goal_kicks=stat['value']
            if stat['name']=='goals_conceded':
                    goals_conceded =stat['value']
            if stat['name']=='error_lead_to_goal':
                    errors_leading_to_goal=stat['value']
            if stat['name']=='own_goals':
                    own_goals=stat['value']
            if stat['name']=='accurate_long_balls':
                    accurate_long_balls=stat['value']
            if stat['name']=='clearance_off_line':
                    clearances_off_line=stat['value']
            if stat['name']=='won_tackle':
                    won_tackles=stat['value']
            if stat['name']=='last_man_tackle':
                    last_man_tackles=stat['value']
            if stat['name']=='ball_recovery':
                    recoveries=stat['value']
            if stat['name']=='duel_won':
                    duels_won=stat['value']
            if stat['name']=='duel_lost':
                    duels_lost=stat['value']
            if stat['name']=='won_contest':
                    successful_50_50s=stat['value']
            if stat['name']=='aerial_won':
                    aerial_battles_won=stat['value']
            if stat['name']=='aerial_lost':
                    aerial_battles_lost=stat['value']
            if stat['name']=='accurate_cross':
                    accurate_crosses=stat['value']
            if stat['name']=='total_through_ball':
                    through_balls=stat['value']
            if stat['name']=='accurate_pass':
                    accurate_passes=stat['value']        
          try:
             goals_per_match=(int(goals)/int(appearences))
          except:
             goals_per_match='no data'
          try:
             shooting_accuracy=(int(shots_on_target)/int(shots))
          except:
             shooting_accuracy='no data'
          try:
             passes_per_match=(int(passes)/int(appearences))
          except:
             passes_per_match='no data'
          try:
             cross_accuracy=(int(accurate_crosses)/int(crosses))
          except:
             cross_accuracy='no data'
          try:
             tackle_success=(int(won_tackles)/int(tackles))
          except:
             tackle_success='no data'
          try:
             pass_accuracy=(int(accurate_passes)/int(passes))
          except:
             pass_accuracy='no data'
          try:
             catches=(int(catches_stand)+int(catches_dive))
          except:
             catches='no data'
        
        dic2={
              
              'player_id':player_id,
              'player_name':name,
              'position':position,
              'shirt_num':shirt_num,
              'position_details':position_details,
              'goals':goals,
              'goals_per_match':goals_per_match,
              'headed_goals':headed_goals,
              'goals_with_right_foot':goals_with_right_foot,
              'goals_with_left_foot':goals_with_left_foot,  
              'penalties_scored':penalties_scored, 
              'freekicks_scored':freekicks_scored, 
              'shots':shots, 
              'shots_on_target':shots_on_target,  
              'shooting_accuracy':shooting_accuracy, 
              'hit_woodwork':hit_woodwork,
              'big_chances_missed':big_chances_missed,
              'assists':assists,
              'passes':passes,
              'passes_per_match':passes_per_match,  
              'pass_accuracy':pass_accuracy,  
              'big_chances_created':big_chances_created,  
              'crosses':crosses,
              'cross_accuracy':cross_accuracy,  
              'accurate_long_balls':accurate_long_balls,  
              'through_balls':through_balls,                
              'yellow_cards':yellow_cards, 
              'red_cards':red_cards,  
              'fouls':fouls, 
              'offsides':offsides,            
              'tackles':tackles, 
              'tackle_success':tackle_success,
              'blocked_shots':blocked_shots,
              'interceptions':interceptions,
              'total_clearances':total_clearances,  
              'head_clearnces':head_clearnces,
              'clean_sheets':clean_sheets,
              'goals_conceded':goals_conceded,    
              'errors_leading_to_goal':errors_leading_to_goal,    
              'own_goals':own_goals,    
              'clearances_off_line':clearances_off_line, 
              'last_man_tackles':last_man_tackles, 
              'recoveries':recoveries, 
              'duels_won':duels_won,
              'duels_lost':duels_lost,
              'successful_50_50s':successful_50_50s,
              'aerial_battles_won':aerial_battles_won,
              'aerial_battles_lost':aerial_battles_lost,
              'saves':saves,
              'penalty_saves':penalty_saves,
              'punches':punches,
              'good_high_claim':good_high_claim,
              'sweeper_clearences':sweeper_clearences,
              'throw_outs':throw_outs,
              'goal_kicks':goal_kicks,
              'catches':catches             
              }
        yield dic2
         