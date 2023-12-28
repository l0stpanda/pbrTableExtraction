from selenium import webdriver    # pip install selenium, pip install webdriver_manager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd    # pip install pandas
import mysql_library
from datetime import datetime


def listMaker(confStandings, confName):
    confList = []
    currentDate = datetime.today().strftime('%Y-%m-%d')

    for tr in confStandings.find_elements(By.XPATH, 'tbody/tr'):
        team = tr.find_elements(By.TAG_NAME, 'a')[0].text
        tds = tr.find_elements(By.TAG_NAME, 'td')
        wins = tds[2].text
        losses = tds[3].text

        confList.append({'conf': confName, 'team': team, 'wins': wins, 'losses': losses, 'date': currentDate})

    return confList

def getBrowser(width=1920, height=1980, headless=False):
    service = Service()
    options = Options()
    
    if headless == True:
        options.add_argument('--headless')

    browser = webdriver.Chrome(service = service, options = options)
    browser.set_window_size(width, height)
    return browser

if __name__ == '__main__':
    browser = None
    try:
        browser = getBrowser()
        browser.get("https://www.basketball-reference.com/")

        eStandings = browser.find_element(By.ID, 'confs_standings_E')
        wStandings = browser.find_element(By.ID, 'confs_standings_W')

        eastList = listMaker(eStandings, 'East')
        westList = listMaker(wStandings, 'West')

        print(eastList)
        print(westList)

        df = pd.DataFrame(eastList + westList)

        mysql = mysql_library.mysql_library('root', 'tigertiger', 'localhost', 'nba')
        createTableQuery = '''CREATE TABLE IF NOT EXISTS nbaRecords (
                                  conf varchar(64), 
                                  team varchar(64),
                                  wins int, 
                                  losses int,
                                  date date,
                                  CONSTRAINT pk_nbaRecords PRIMARY KEY(team, date)
                                  );
                            '''
        mysql.execute_sql_schema(createTableQuery)
        mysql.insert_df_into_table(df, 'nbaRecords')

        print("Success")
    except Exception as ex:
        print(ex)
    finally:
        if not browser is None:
            browser.quit()