import pandas
import webbrowser
import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import re
import os
import random
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# input: input.xlsx file
# update chrome to the l

# This function gets the list from the excel file
# it will return an [{code: , msa: , name: },{}] format.
def get_from_excel_file():
    df = pandas.read_excel('input.xlsx')

    # print the column names
    total_scrap_array = []
    excel_format = {"code": "", "msa": "", "name": ""}
    # get the values for a given column
    # values = df['code',"msa","name"].values
    # print(values)
    code = df['code']
    msa = df['msa']
    name = df['name']
    for x in range(len(code)):
        excel_format = {"code": "", "msa": "", "name": "", "searching": ""}
        excel_format["code"] = code[x]
        excel_format["msa"] = msa[x]
        excel_format["name"] = name[x]
        tempstring = str(name[x])
        tempstring = tempstring.replace(" ", "_")
        tempstring = tempstring.replace(",", "_")
        excel_format["searching"] = tempstring
        total_scrap_array.append(excel_format)

    # print(total_scrap_array)
    return total_scrap_array


def get_to_the_go_rental(driver, cityname):
    url = "https://www.gosection8.com/Tenant/tn_Results.aspx?Address="
    newurl = url + cityname
    print(newurl + "  is presented..........\n")
    # Go to example.com
    driver.get(newurl)
    time.sleep(np.random.lognormal(0, 1))
    soup = BeautifulSoup(driver.page_source, "lxml")
    print("waiting 5 sec for opening the website")
    time.sleep(np.random.lognormal(0, 1))
    info = soup.find("div", {"class": "noresults"})

    if info == None:

        pageLinks = []

        pageRange = soup.find("div", {"id": "MainContentPlaceHolder_paging"})
        checkChild = pageRange.find("ul", recursive=False)
        if checkChild:
            children = pageRange.find("ul", recursive=False).findAll("li")
            if len(children) > 1:
                rangeOfPage = int(children[-2].getText())
                # page starts from 0 ~ rangeofPage - 1 by adding &pg=0 ~ rangeofPage

                pageUrl = "&pg="
                for pages in range(rangeOfPage):
                    urlWithPages = newurl + pageUrl + str(pages)
                    pageLinks.append(urlWithPages)
            else:
                urlWithPages = newurl + "&pg=0"
                pageLinks.append(urlWithPages)
        else:
            urlWithPages = newurl + "&pg=0"
            pageLinks.append(urlWithPages)

        eachHouseInfo = getEachHouseHref(driver, pageLinks)
        writeIntoCVS(cityname, eachHouseInfo)

        # &&&&&&&&&&&&&&&
        # need to write into csv
        # &&&&&&&&&&&&&&

    else:
        print(".....................no infomation for this link.....................")


def checkingCVS(d_name, file_name):
    direc = os.path.dirname(d_name)
    if os.path.exists(direc):
        if os.path.exists(d_name + file_name):
            return True
        else:
            return False
    else:
        path = './cvs_outputs'
        os.mkdir(path)
        return False


def withoutDup(file_name, eachHouseInfo):
    alreadyIn = []
    house_id = []
    with open(file_name, "rb") as f:
        csvreader = csv.reader(f, delimiter=",")
        for row in csvreader:
            house_id.append(row[0])
    for eachInfo in eachHouseInfo:
        if eachInfo["u_id"] in house_id:
            alreadyIn.append(eachInfo["u_id"])

    return alreadyIn


def writeIntoCVS(cityname, eachHouseInfo):
    print("\nwriting " + cityname + " into csv under csv_outputs folder\n")
    d_name = './cvs_outputs/'
    file_name = cityname + '.csv'
    check = checkingCVS(d_name, file_name)
    fieldnames = ["u_id", "address", "ptype", "rent",
                  "deposit", "bed", "bath", "sqfeet", "yearbuilt", "pet",
                  "ceilingFan", "furnished", "fireplace", "cablePaid",
                  "securitySystem", "laundry", "washer", "dryer",
                  "heatstyle", "dishwasher", "stove", "garbage", "refrigerator",
                  "microwave", "swimming", "parking", "fence", "porch", "smoking"]
    if check:
        alreadyIn = withoutDup(file_name, eachHouseInfo)
        with open(dname + file_name, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for info in eachHouseInfo:
                if info["u_id"] not in alreadyIn:
                    writer.writerow(info)
    else:
        with open(d_name + file_name, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for info in eachHouseInfo:
                writer.writerow(info)


def getEachHouseHref(driver, pageLinks):
    print("\ngetting the each house links for scrap\n")
    eachHouseHref = []
    for page in pageLinks:
        driver.get(page)
        time.sleep(np.random.lognormal(0, 1))
        soup = BeautifulSoup(driver.page_source, "lxml")
        for link in soup.findAll("a", {"class": "resultslearnmore"}):
            eachHouseHref.append("https://www.gosection8.com" + link.get('href'))

    return getInformationOfHouse(driver, eachHouseHref)


def getInformationOfHouse(driver, links):
    print("\ngetting the information for each house\n")
    totalArray = []
    for link in links:
        driver.get(link)
        time.sleep(np.random.lognormal(0, 1))
        soup = BeautifulSoup(driver.page_source, "lxml")
        u_id = link[-7:]
        address = ""
        for addr in soup.findAll("span", {"class": "address"}):
            address += addr.getText()
        # freeRentAmount = soup.find("span", {"id" : "MainContentPlaceHolder_freeRentAmount"}).getText()
        ptype = soup.find("span", {"id": "MainContentPlaceHolder_ptype"}).getText()
        rent = soup.find("span", {"id": "MainContentPlaceHolder_rdep"}).getText()
        deposit = soup.find("span", {"id": "MainContentPlaceHolder_rdep2"}).getText()
        bed = soup.find("span", {"id": "MainContentPlaceHolder_bb"}).getText()
        bath = soup.find("span", {"id": "MainContentPlaceHolder_bb2"}).getText()
        sqfeet = soup.find("span", {"id": "sqft"}).getText()
        yearbuilt = soup.find("span", {"id": "yb"}).getText()
        pet = soup.find("span", {"id": "MainContentPlaceHolder_IsPet"}).getText()
        ceilingFan = soup.find("span", {"id": "MainContentPlaceHolder_ceiling"}).getText()
        furnished = soup.find("span", {"id": "MainContentPlaceHolder_Furnish"}).getText()
        fireplace = soup.find("span", {"id": "MainContentPlaceHolder_fire"}).getText()
        cablePaid = soup.find("span", {"id": "MainContentPlaceHolder_cable"}).getText()
        securitySystem = soup.find("span", {"id": "MainContentPlaceHolder_ss"}).getText()
        laundry = soup.find("span", {"id": "MainContentPlaceHolder_laund"}).getText()
        washer = soup.find("span", {"id": "MainContentPlaceHolder_washer"}).getText()
        dryer = soup.find("span", {"id": "MainContentPlaceHolder_dryer"}).getText()
        heatstyle = soup.find("span", {"id": "MainContentPlaceHolder_heatstyle"}).getText()
        dishwasher = soup.find("span", {"id": "MainContentPlaceHolder_dw"}).getText()
        stove = soup.find("span", {"id": "MainContentPlaceHolder_stove"}).getText()
        garbage = soup.find("span", {"id": "MainContentPlaceHolder_gd"}).getText()
        refrigerator = soup.find("span", {"id": "MainContentPlaceHolder_refrig"}).getText()
        microwave = soup.find("span", {"id": "MainContentPlaceHolder_micro"}).getText()
        swimming = soup.find("span", {"id": "MainContentPlaceHolder_pool"}).getText()
        parking = soup.find("span", {"id": "MainContentPlaceHolder_park"}).getText()
        fence = soup.find("span", {"id": "MainContentPlaceHolder_fy"}).getText()
        porch = soup.find("span", {"id": "MainContentPlaceHolder_ext"}).getText()
        smoking = soup.find("span", {"id": "MainContentPlaceHolder_smoking"}).getText()
        time.sleep(np.random.lognormal(0, 1))
        diction = {"u_id": u_id, "address": address, "ptype": ptype, "rent": rent,
                   "deposit": deposit, "bed": bed, "bath": bath, "sqfeet": sqfeet, "yearbuilt": yearbuilt, "pet": pet,
                   "ceilingFan": ceilingFan, "furnished": furnished, "fireplace": fireplace, "cablePaid": cablePaid,
                   "securitySystem": securitySystem, "laundry": laundry, "washer": washer, "dryer": dryer,
                   "heatstyle": heatstyle, "dishwasher": dishwasher, "stove": stove, "garbage": garbage, "refrigerator": refrigerator,
                   "microwave": microwave, "swimming": swimming, "parking": parking, "fence": fence, "porch": porch, "smoking": smoking}
        totalArray.append(diction)
    return totalArray


chromedriver = "/usr/local/bin/chromedriver"  # path to the chromedriver executable
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))
sys.path.append(chromedriver)

driver = webdriver.Chrome(chromedriver)
time.sleep(np.random.lognormal(0, 1))

names = get_from_excel_file()
for county in names:
    print("working on the " + county['searching'] + " to scrap")
    get_to_the_go_rental(driver, county["searching"])
driver.close()

