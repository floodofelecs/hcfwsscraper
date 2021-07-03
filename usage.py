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


#Get all sensor numbers and names and then read that file creating a map of sensor number to sensor name
# Create a function that 

def split_sens_to_num_name(location_name):
    """
    A function that takes a sensor full name and splits it into a number and a sensor name
    The funtcion only returns the first 30 charcters in the sensor name to issues when saving the files/sheetnames.

    Return:
        sensor_num: The sensor number as an integer
        sensor_name: The sensor name only as a string
    """
    split_loc_name = location_name.split(":", 1)
    sensor_num = split_loc_name[0].strip()
    sensor_name = split_loc_name[1].strip().replace(sensor_num, '')
    sensor_name = sensor_name[:29].strip()

    return sensor_num, sensor_name



df1 = pd.read_csv("/Users/mohamedabead/Desktop/vip/data/sensor_num_to_name2.csv")
# print(df1)




# # df1.reset_index(drop=True, inplace=True)
# arr = []
# for i in range (96, 134):
#     arr.append(i)

# update_df = df1.drop(arr)
# # df1 = df1.drop(arr)
# update_df.reset_index(drop=True, inplace=True)
# # print(update_df)

# cols = list(update_df.columns.values)

# # update_df.drop([cols[0]])
# print(cols)

# update_df = update_df.drop(columns=[cols[0]])

# update_df.to_csv("/Users/mohamedabead/Desktop/vip/data/sensor_num_to_name2.csv")
# print(update_df)