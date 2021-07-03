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


# Assigning sensors their locations according to the excel sheets published by the harris county flood warning system monthly reports
sens_num_loc = {
    "100":"Clear Creek", "110":"Clear Creek", "120":"Clear Creek","130":"Clear Creek", "135":"Clear Creek", "150":"Clear Creek","170":"Clear Creek",
    "175":"Clear Creek", "180":"Clear Creek", "190":"Clear Creek",
    "105":"Clear Creek Tributaries", "115":"Clear Creek Tributaries", "125":"Clear Creek Tributaries", "140":"Clear Creek Tributaries",
    "160":"Clear Creek Tributaries", "200":"Clear Creek Tributaries", "610":"Clear Creek Tributaries",
    "210":"Armand Bayou and Tributaries", "220":"Armand Bayou and Tributaries", "230":"Armand Bayou and Tributaries",
    "240":"Armand Bayou and Tributaries", "245":"Armand Bayou and Tributaries", "250":"Armand Bayou and Tributaries", "270":"Armand Bayou and Tributaries",
    "310":"Sims and Vince Bayou", "320":"Sims and Vince Bayou", "340":"Sims and Vince Bayou", "360":"Sims and Vince Bayou", "370":"Sims and Vince Bayou",
    "380":"Sims and Vince Bayou", "910":"Sims and Vince Bayou", "920":"Sims and Vince Bayou", "940":"Sims and Vince Bayou",
    "400":"Brays and Keegans Bayou", "405":"Brays and Keegans Bayou", "410":"Brays and Keegans Bayou", "420":"Brays and Keegans Bayou", 
    "430":"Brays and Keegans Bayou", "435":"Brays and Keegans Bayou", "440":"Brays and Keegans Bayou", "445":"Brays and Keegans Bayou", 
    "460":"Brays and Keegans Bayou", "465":"Brays and Keegans Bayou", "470":"Brays and Keegans Bayou", "475":"Brays and Keegans Bayou", 
    "485":"Brays and Keegans Bayou", "1020":"Brays and Keegans Bayou", 
    "480":"Keegans Bayou", "490":"Keegans Bayou", "495":"Keegans Bayou", 
    "510":"White Oak Bayou and Tributaries", "520":"White Oak Bayou and Tributaries", "530":"White Oak Bayou and Tributaries", 
    "535":"White Oak Bayou and Tributaries", "540":"White Oak Bayou and Tributaries", "545":"White Oak Bayou and Tributaries", 
    "550":"White Oak Bayou and Tributaries", "555":"White Oak Bayou and Tributaries", "560":"White Oak Bayou and Tributaries", 
    "570":"White Oak Bayou and Tributaries", "575":"White Oak Bayou and Tributaries", "580":"White Oak Bayou and Tributaries", 
    "582":"White Oak Bayou and Tributaries", "585":"White Oak Bayou and Tributaries", "590":"White Oak Bayou and Tributaries", 
    "595":"White Oak Bayou and Tributaries", "1000":"White Oak Bayou and Tributaries", 
    "605":"Cedar and Little Cedar Bayou and Goose Creek", "620":"Cedar and Little Cedar Bayou and Goose Creek", 
    "640":"Cedar and Little Cedar Bayou and Goose Creek", "650":"Cedar and Little Cedar Bayou and Goose Creek", 
    "660":"Cedar and Little Cedar Bayou and Goose Creek", "1520":"OutOfService", 
    "1540":"Cedar and Little Cedar Bayou and Goose Creek", "1720":"Cedar and Little Cedar Bayou and Goose Creek", 
    "1725":"Cedar and Little Cedar Bayou and Goose Creek", "1730":"Cedar and Little Cedar Bayou and Goose Creek", 
    "1740":"Cedar and Little Cedar Bayou and Goose Creek", "1745":"Cedar and Little Cedar Bayou and Goose Creek", 
    "710":"Luce and Jackson Bayou and San Jacinto", "720":"Luce and Jackson Bayou and San Jacinto", "740":"Luce and Jackson Bayou and San Jacinto", 
    "750":"Luce and Jackson Bayou and San Jacinto", "755":"Luce and Jackson Bayou and San Jacinto", "760":"Luce and Jackson Bayou and San Jacinto", 
    "765":"Luce and Jackson Bayou and San Jacinto", "770":"OutOfService", "780":"Luce and Jackson Bayou and San Jacinto", 
    "785":"Luce and Jackson Bayou and San Jacinto", "790":"Luce and Jackson Bayou and San Jacinto", "795":"Luce and Jackson Bayou and San Jacinto", 
    "1840":"Luce and Jackson Bayou and San Jacinto", "1930":"Luce and Jackson Bayou and San Jacinto", "1940":"Luce and Jackson Bayou and San Jacinto", 
    "1960":"Luce and Jackson Bayou and San Jacinto", "1975":"Luce and Jackson Bayou and San Jacinto", 
    "820":"Hunting and Carpenters Bayou", "830":"Hunting and Carpenters Bayou", "840":"Hunting and Carpenters Bayou", 
    "1420":"Hunting and Carpenters Bayou", "1440":"Hunting and Carpenters Bayou", "1460":"Hunting and Carpenters Bayou", 
    "1040":"Spring and Willow Creek", "1050":"Spring and Willow Creek", "1052":"Spring and Willow Creek", "1054":"Spring and Willow Creek", 
    "1055":"Spring and Willow Creek", "1056":"Spring and Willow Creek", "1060":"Spring and Willow Creek", "1070":"Spring and Willow Creek", 
    "1072":"Spring and Willow Creek", "1074":"Spring and Willow Creek", "1075":"Spring and Willow Creek", "1076":"Spring and Willow Creek", 
    "1080":"Spring and Willow Creek", "1084":"Spring and Willow Creek", "1086":"Spring and Willow Creek", "1090":"Spring and Willow Creek", 
    "1320":"Spring and Willow Creek", "1340":"Spring and Willow Creek",
    "1110":"Cypress Creek", "1115":"Cypress Creek", "1120":"Cypress Creek", "1130":"Cypress Creek", "1140":"Cypress Creek", 
    "1150":"Cypress Creek", "1160":"Cypress Creek", "1165":"Cypress Creek", "1170":"Cypress Creek", "1175":"Cypress Creek", 
    "1180":"Cypress Creek", "1185":"Cypress Creek", "1186":"Cypress Creek", "1190":"Cypress Creek", "1195":"Cypress Creek", 
    "1210":"Little Cypress Creek", "1220":"Little Cypress Creek", "1230":"Little Cypress Creek", 
    "1600":"Greens Bayou", "1610":"Greens Bayou", "1620":"Greens Bayou", "1640":"Greens Bayou", "1645":"Greens Bayou", "1660":"Greens Bayou", 
    "1665":"Greens Bayou", "1670":"Greens Bayou", "1685":"Greens Bayou", "1695":"Greens Bayou", 
    "1630":"Halls and Garners Bayou", "1650":"Halls and Garners Bayou", "1655":"Halls and Garners Bayou", "1675":"Halls and Garners Bayou", 
    "1680":"Halls and Garners Bayou", "1690":"Halls and Garners Bayou", 
    "2010":"Addicks and Barker Reservoir", "2015":"Addicks and Barker Reservoir", "2020":"Addicks and Barker Reservoir", "2025":"Addicks and Barker Reservoir", 
    "2030":"Addicks and Barker Reservoir", "2040":"Addicks and Barker Reservoir", "2050":"Addicks and Barker Reservoir", "2060":"Addicks and Barker Reservoir", 
    "2090":"Addicks and Barker Reservoir", "2110":"Addicks and Barker Reservoir", "2120":"Addicks and Barker Reservoir", "2130":"Addicks and Barker Reservoir", 
    "2140":"Addicks and Barker Reservoir", "2150":"Addicks and Barker Reservoir", "2160":"Addicks and Barker Reservoir", "2170":"Addicks and Barker Reservoir", 
    "2180":"Addicks and Barker Reservoir", "2190":"Addicks and Barker Reservoir", 
    "2210":"Buffalo Bayou", "2220":"Buffalo Bayou", "2240":"Buffalo Bayou", "2250":"Buffalo Bayou", "2253":"Buffalo Bayou", "2255":"Buffalo Bayou", 
    "2260":"Buffalo Bayou", "2265":"Buffalo Bayou", "2270":"Buffalo Bayou", "2280":"Buffalo Bayou", "2290":"Buffalo Bayou", 
}

sens_num_to_loc = defaultdict(int)

for key in sens_num_loc.keys():
    sens_num_to_loc[key] = sens_num_loc[key]

def get_bayou_using_num(sensor_number):
    """
    A function that returns the bayou given sesnor number
    """
    sensor_number = str(sensor_number)

    return sens_num_loc[sensor_number]


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



def get_sensor_name(sensor_number):
    """
    A function that returns the sensor name(first 29 characters) given the sensor number
    """
    df = pd.read_csv("/Users/mohamedabead/Desktop/vip/data/sensor_num_to_name2.csv")
    d2 = df[df["Number"] == sensor_number]
    return d2["Name"].values[0]


def get_min_intervals():
    """
    A function that takes input from the user and returns the amount in minutes approximated to 5-minute

    Returns:
        no_of_intervals - number of intervals to get 
    """
    print("You want data for last (how many days): ")
    print("Enter days: ")
    days = int(input())
    print("Enter Hours: ")
    hrs = int(input())
    print("Enter Minutes(5-minute): ")
    mins = int(input())

    total_mins = days * 24 * 60
    total_mins += hrs * 60 
    total_mins += mins

    no_of_intervals= total_mins // 5

    return no_of_intervals


def visualize(sensor_number):
    """
    Visulaize the number of intervals for the sensor number 
    """
    intervals = get_min_intervals()
    filename_loc = "/Users/mohamedabead/Desktop/vip/data/" +  str(sens_num_to_loc[str(sensor_number)]) + ".xlsx"
    sensor_name = get_sensor_name(sensor_number)
    print("*"+ sensor_name + "*")
    # df = pd.read_excel(filename_loc, sheet_name=)
    



#TESTING
# YOU NEED TO REVERSE THE ORDER OF APPENDING DATA TO HAVE IT IN ORDER
# Get sesnor 520: White Oak Bayou @ Heights Bo
# 7/2/2021 6:30 PM 0.28"

# get_min_intervals()
visualize(520)


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