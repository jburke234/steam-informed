# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 11:54:50 2020

@author: yea-b
"""

import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import geckodriver_autoinstaller

# ===============================================================================================
# ===============================================================================================
# 
#   This script scraps a list of steam id numbers of public profiles from https://steamtime.info/ 
#   Outputs said list to a text file, to be used to gather data using the steam API    
# 
# ===============================================================================================
# ===============================================================================================




# =============================================================================
# 
#   Accept the cookie policy as the select is obscured by it    
# 
# =============================================================================
def click_cookie(driver):
    try:
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[1]/div/div[2]/button[2]"))).click()
        cookie_accept = driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div/div[2]/button[2]').click()
    except:
        print('Did not find cookie accept')
        return False
    
    return True


# =============================================================================
# 
#   Select the dropdown -> set table size to 100   
# 
# =============================================================================
def set_dropdown(driver):
    try:
        select_dropdown = Select(driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[4]/div/div[2]/div[1]/label/select"))
        select_dropdown.select_by_value('100')
        
    except:
        print("Could not locate dropdown")
        return False
    
    return True


# =============================================================================
# 
#   Select dynamic table and return it's HTML as a string
# 
# =============================================================================
def select_table(driver):
    try:
        #//*[@id="ranking-table_wrapper"] //*[@id="ranking-table"]x path('/html/body/div[5]/div[2]/div[4]')
        element = driver.find_element_by_id('ranking-table')
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
        if "data-steamid" in line:
            result = re.search('data-steamid="(.*)"', line)
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
    file = open('steam_ids.txt', 'w')

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
    URL = 'https://steamtime.info/'
    
    driver.get(URL)
    
    # Used to ensure all conditions are met (cookies accepted, table size set to 100 and html converted to a string)
    overall_control = False
    
    cookie_control = click_cookie(driver)
    
    dropdown_control = set_dropdown(driver)
    
    table_element = select_table(driver)
    
    if((cookie_control== True) and (dropdown_control == True) and (len(table_element) > 1)):
       overall_control = True
       
    # Recursive call to main to ensure all controls are met
    while(overall_control != True):
        driver.close()
        main()
    
    list_of_id_nums = parse_info(table_element)
    
    write_to_file(list_of_id_nums)
    
    # Output array of steam id nums
    print(list_of_id_nums)
    print(len(list_of_id_nums))


    
if __name__ == '__main__':
    main()