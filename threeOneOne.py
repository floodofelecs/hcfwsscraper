from re import split
from collections import defaultdict
from datetime import date
import csv
from re import sub
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
from openpyxl import load_workbook


# # Create a web driver using chrome webdriver and send the link of the website to that driver
# driver = webdriver.Chrome()

# my_url = "https://hfdapp.houstontx.gov/311/311-Public-Data-Extract-2020-clean.txt"

# driver.get(my_url)

# #Getting current page parsed html using beautifulsoup
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'lxml')

# # time.sleep(120)
# # print("Did it work???")

# entire_text = soup.find("pre").text

# file1 = open("threeOneOne.txt","w")
# file1.write(entire_text)
# file1.close()

# # panda_df = pd.DataFrame(entire_text)

# # panda_df.to_csv("/Users/mohamedabead/Desktop/vip/threeoneone.csv")

# # print(entire_text)


# driver.quit()





















# Using readlines()
file1 = open('threeOneOne.txt', 'r')
Lines = file1.readlines()
titles = Lines[0]
titles = titles.split("|")

dict = defaultdict(int)
num_to_title = defaultdict(int)
title_to_num = defaultdict(int)

counter = 0
for title in titles:
    title = title.replace("\n", "")
    # print(title)
    num_to_title[counter] = title
    title_to_num[title] = counter
    counter += 1
    dict[title] = []

# print(num_to_title)

for i in range(1, len(Lines)):
    #Taking all cells in a row of data
    cells = Lines[i]
    cells = cells.split("|")
    # counter = 0
    # For every cell
    # if "Flooding" in cells[14]: 
    if cells[15] == "Flooding":
        for j in range(len(cells)):
            #Make sure it doesn't have the end of line 
            cells[j] = cells[j].replace("\n", "")
            # Add the cell to under the appropriate title
            title = num_to_title[j]
            dict[title].append(cells[j])
    
            


panda_df = pd.DataFrame(dict)

# print(panda_df.head())
# panda_df.to_csv("threeOneOne.csv", index=False)
panda_df.to_csv("threeOneOne.csv", mode='a', index=False, header=False)

# print(dict)

