from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests
import CONSTANTS_FLASHSCORE
import time
import sqlite3
import dbManagerFlashscore
import flashscore_scraperUtilities
from main import sendMessageToAdmin
from selenium.webdriver.firefox.options import Options


def run():
    driver = webdriver.Chrome(executable_path=r'C:\WebDriver\chromedriver.exe')


    try:
        for sport in CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS.keys():
            print("fetching data for "+ sport+ "....")
            for competition in CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS[sport]:

                url =CONSTANTS_FLASHSCORE.BASE_URL + sport+"/"+competition+"fixtures/"
                driver.get(url)

                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, "html.parser")

                matchesToSave = []
                for el in soup.find_all("div",class_="event__match"):
                    match = flashscore_scraperUtilities.generateMatch(el,sport,competition)

                    if(flashscore_scraperUtilities.mustSaveMatch(match)):
                        matchesToSave.append(match)

                dbManagerFlashscore.clearMatches(CONSTANTS_FLASHSCORE.FLASCORE_SPORTS_NAMING[sport],
                CONSTANTS_FLASHSCORE.FLASCORE_COMPETITIONS_NAMING[str(sport + " "+ competition)])
                dbManagerFlashscore.insertMatches(matchesToSave)

        sendMessageToAdmin("Updated finished succesfully!")

        return
    except Exception as e:
        sendMessageToAdmin("Error on update!")
    return