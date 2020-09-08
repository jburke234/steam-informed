# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:41:28 2020

@author: yea-b
"""


import requests
import json
#import pandas as pd
#from pandas import ExcelWriter
from datetime import date
from pathlib import Path
import os

# =============================================================================
# 
#       Writes the aggregate of all players' data from a game
#       to a dated json file    
# 
# =============================================================================
def write_to_file(game_name, today, game_stat_json):
    file_name = game_name + str(today) + ".json"
    
    with open(file_name,'w') as file:
        #json.dump(game_stat_json,file, indent = 4, sort_keys =True)
        file.write(str(game_stat_json))
    
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
#       Builds and executes an API query to retrieve player stats. 
#       Formats and returns the stats in a dictionary 
# 
# =============================================================================
def steam_player_stats(game_id, user_id, steam_api_key, stats, today): 
    
    # Build Query string 
    steam_api_url_part_1 = 'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key='
     
    steam_api_game_id = game_id
    
    steam_api_url_part_2 = '&appid='
     
    steam_api_url_part_3 = '&steamid='
    
    steam_test_user_id = user_id
    
    steam_api_url_complete = steam_api_url_part_1 + steam_api_key  + steam_api_url_part_2 + steam_api_game_id  + steam_api_url_part_3 + steam_test_user_id
    
    # Request info from the API
    response = requests.get(steam_api_url_complete)
    
    # Generate json from the response
    parsed = json.loads(response.text)
    
    stats_json = parsed["playerstats"]["stats"]
    
    player_stat_dict = dict()    
    
    # Add user_id and date to the dictionary 
    player_stat_dict["steam_id"] = user_id
    player_stat_dict["date"] = today
    
    # Loop through the stats and json objects to create a dictionary of stat: value key pairs
    for stat in stats:
        
        for elem in stats_json:
            
            if stat == elem["name"]:
                
                val = elem["value"]
                
                player_stat_dict[stat] = val
                
    
    return player_stat_dict


# =============================================================================
# 
#       Checks game id to return game name and control for file path 
# 
# =============================================================================       
def check_game_id(game_id):
    if game_id == '730':
        game_name = "CSGO"
        control= 0
    elif game_id == '440':
        game_name = "TF2"
        control = 1
    else:
        game_name = "GM"
        control = 2
        
    return control, game_name

    
# =============================================================================
# 
#       Takes two lists and combines them into 1 with no duplicates 
# 
# =============================================================================
def combine_two_lists_no_dup(list_one, list_two):
    
    first = set(list_one)
    second = set(list_two)
    
    temp = second - first
    
    result = list_one + list(temp)
    
    return result
    
    
# =============================================================================
# 
#       Main 
# 
# =============================================================================
def main():
    
    today = date.today()
    
    steam_api_key = 'XXXXXXXX'
    
    file_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\Scraping\steam_ids.txt")
    list_of_steamtime_ids = read_file(file_path) 
    
    file_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\Scraping\steam_ids_steamdb.txt")
    list_of_steamdb_ids = read_file(file_path) 
    
    file_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\GetGameSchema\game_ids.txt")
    list_of_game_ids = read_file(file_path) 
    
    csgo_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\GetGameSchema\ValveTestApp260.txt")
    
    tf2_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\GetGameSchema\Team Fortress 2.txt")
    
    gm_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\GetGameSchema\Garry's Mod.txt")
    
    file_list = [csgo_path, tf2_path, gm_path]    
    
    list_of_user_ids = combine_two_lists_no_dup(list_of_steamtime_ids, list_of_steamdb_ids)
    
    # Loops through each game 
    for game_id in list_of_game_ids:
        
        # Check which game is need for the corresponding file to be read
        control, game_name = check_game_id(game_id)
        
        # Gets the corresponding game stats from a file 
        stats = read_file(file_list[control])
        
        # Holds all player stats for this game
        game_stat_json = dict()
        
        # Loops through each user for this game and adds stats to game_stat_json
        for user_id in list_of_user_ids:
            
            try:
                player_stat_dict = steam_player_stats(game_id, user_id, steam_api_key, stats, today)
                
                game_stat_json[user_id] = player_stat_dict
                
            except:
                print("Error getting data for ", "game id: ", game_id, " user_id: ", user_id)
                
        write_to_file(game_name, today, game_stat_json)


if __name__ == '__main__':
    main()
