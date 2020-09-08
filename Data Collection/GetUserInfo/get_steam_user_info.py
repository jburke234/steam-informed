# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:18:55 2020

@author: yea-b
"""

import requests
import json
from pathlib import Path

# =============================================================================
# 
#       Writes the dictionary to a json file    
# 
# =============================================================================
def write_to_file(id_and_username_dict):
    
    with open('steam_user_info.json','w') as file:
        json.dump(id_and_username_dict,file)
    
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
#       Takes the steam id and requests the player summary from the steam API 
#       Returns username   
# 
# =============================================================================
def steamProfile(user_id, steam_api_key):
    
    steam_api_url_part_1 = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key='

    steam_api_url_part_2 = '&steamids='

    steam_user_id = user_id

    steam_api_url_complete = steam_api_url_part_1 + steam_api_key + steam_api_url_part_2 + steam_user_id

    response = requests.get(steam_api_url_complete)

    parsed = json.loads(response.text)
    
    username = parsed["response"]["players"][0]["personaname"]
    
    return username



# =============================================================================
# 
#       Steam profile    
# 
# =============================================================================
def main():
    
    steam_api_key = 'XXXXXXXXX'
    
    file_path = Path(r"C:\Users\yea-b\Desktop\Steam Web App\Scraping\steam_ids.txt")
    
    list_of_ids = read_file(file_path)
    
    id_and_username_dict = dict()
    
    for id_num in list_of_ids:
        username = steamProfile(id_num, steam_api_key)
        id_and_username_dict[id_num] = username
    
    write_to_file(id_and_username_dict)


if __name__ == '__main__':
    main()
