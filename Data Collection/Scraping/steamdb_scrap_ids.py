# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:18:21 2020

@author: yea-b
"""


# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:54:50 2020

@author: yea-b
"""

import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import geckodriver_autoinstaller
import time

# ==============================================================================================================
# ==============================================================================================================
# 
#   This script scraps a list of steam id numbers of public profiles from https://steamdb.info/stats/toplevels/
#   Outputs said list to a text file, to be used to gather data using the steam API    
# 
# ==============================================================================================================
# ==============================================================================================================


# =============================================================================
# 
#   Select dynamic table and return it's HTML as a string
# 
# =============================================================================
def select_table(driver):
    try:
        element = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[5]/table')
        
    except:
         print('Did not find table')
         return ""
    
    table_element = ""
    
    # Split the HTML into lines of a string
    element_html = element.get_attribute('innerHTML')
    table_element =  str(element_html).splitlines()
    
    return table_element


# =============================================================================
# 
#   Parses and returns a list of id nums from the string 
# 
# =============================================================================
def parse_info(table_element):
    list_of_id_nums = list()

    # Get steam id num from table row
    for line in table_element: 
        if "<tr id" in line:
            result = re.search('id="(.*)"', line)
            group = result.group(1)
        
            sub_group = group.split('"',1)
        
            list_of_id_nums.append(sub_group[0])
    
    return list_of_id_nums


# =============================================================================
# 
#   Write list of id nums to a file 
# 
# =============================================================================
def write_to_file(list_of_id_nums):
    file = open('steam_ids_steamdb.txt', 'w')

    for elem in list_of_id_nums:
        file.write('%s\n' % elem)

    file.close


# =============================================================================
# 
#   Main method - controls the flow of the program
# 
# =============================================================================
def main():
    
    geckodriver_autoinstaller.install()
    
    driver = webdriver.Firefox()
    URL = 'https://steamdb.info/stats/toplevels/'
    
    driver.get(URL)   
    
    time.sleep(3)
    
    table_element = select_table(driver)
        
    # Recursive call to main to ensure controls are met
    while(len(table_element) < 1):
        driver.close()
        main()
    
    list_of_id_nums = parse_info(table_element)
    
    # Output array of steam id nums
    write_to_file(list_of_id_nums)
    


    
if __name__ == '__main__':
    main()