# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:27:36 2020

@author: yea-b
"""
import requests
import json
from pathlib import Path


# =============================================================================
# 
#       Writes the list of stat names to a file    
# 
# =============================================================================
def write_to_file(game, stats_json):
    
    game_name = str(game["gameName"]) + ".txt"
    
    list_of_stats = list()
    
    for stat in stats_json:
        list_of_stats.append(stat["name"])
    
    #with open(game_name,'w') as file:
        #for key in stats_json:
    
    file = open(game_name,'w')

    # Write out list of Stat names
    for elem in list_of_stats:
        file.write('%s\n' % elem)
            
    # Write out json    
    #with open(game_name,'w') as file:
        #json.dump(stats_json,file, indent = 4, sort_keys =True)
    
    file.close()


# =============================================================================
# 
#       Reads the id numbers from a file and returns a list    
# 
# =============================================================================
def read_file(file_path):
    
    file = open(file_path,'r')
    
    list_of_ids = list()
    
    for line in file:
        list_of_ids.append(line.replace('\n', ''))
    
    file.close()
    
    return list_of_ids


# =============================================================================
# 
#       Reads the id numbers from a file and returns a list    
# 
# =============================================================================
def getGameStatsSchema(game_id, steam_api_key): 

    steam_api_url_part_1 = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key='

    steam_api_url_part_2 = '&appid='

    steam_api_query = steam_api_url_part_1 + steam_api_key + steam_api_url_part_2 + game_id

    response = requests.get(steam_api_query)
    
    parsed = json.loads(response.text)
    game = parsed["game"]
    
    stats_json = parsed["game"]["availableGameStats"]["stats"]
    

    return game, stats_json
    
    
    
# =============================================================================
# 
#       Steam profile    
# 
# =============================================================================
def main():
    
    steam_api_key = 'XXXXXXXXXXXXXXXXX'
    
    file_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\GetGameSchema\game_ids.txt")
    
    list_of_ids = read_file(file_path) 
    
    for game_id in list_of_ids:
        try:
            game, stats_json = getGameStatsSchema(game_id, steam_api_key)
            write_to_file(game, stats_json)
        except:
            print("Error getting data for id: ", game_id)

if __name__ == '__main__':
    main()
