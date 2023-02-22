from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import CONSTANTS_FLASHSCORE
import time
import sqlite3
import dbManagerFlashscore
from flashscore_scraperUtilities import *



def run():

    
    for sport in CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS.keys():
        print("fetching data for "+ sport+ "....")
        for competition in CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS[sport]:
            driver = webdriver.Chrome()

            url =CONSTANTS_FLASHSCORE.BASE_URL + sport+"/"+competition+"fixtures/"
            driver.get(url)

            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            matchesToSave = []
            for el in soup.find_all("div",class_="event__match"):
                match = generateMatch(el,sport,competition)

                if(mustSaveMatch(match)):
                    matchesToSave.append(match)

            dbManagerFlashscore.clearMatches(CONSTANTS_FLASHSCORE.FLASCORE_SPORTS_NAMING[sport],
            CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS_NAMING[str(sport + " "+ competition)])
            dbManagerFlashscore.insertMatches(matchesToSave)
    return



run()