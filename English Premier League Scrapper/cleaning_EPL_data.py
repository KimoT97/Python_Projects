# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 01:11:53 2022

@author: mrkim
"""

#Cleaning EPL DATA

import json
import numpy as np
import pandas as pd

dict_main={}
dict_stats={}

players = open('EPL_Final.json')
players_data = json.load(players)

i=0
j=0

for player in players_data:
    if 'player_name' in player.keys():
        dict_stats[j]=(player)
        j+=1
    else:
        dict_main[i]=(player)
        i+=1
        
df_main = (pd.DataFrame(dict_main)).transpose()
df_stats = (pd.DataFrame(dict_stats)).transpose()

df_final=pd.merge(df_main, df_stats, on='player_id')