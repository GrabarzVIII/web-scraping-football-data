import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(number):
    # Function to scrape soccer seasons data from PZPN website
    opts = Options()
    opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=opts)
    driver.get(r"https://www.soccerstand.com/pl/pilka-nozna/polska/pko-bp-ekstraklasa-{}-{}/tabela/".format(number[0],number[1]))
    
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.tableCellParticipant__name")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    table_data = []
    
    # Extracting header data
    table_header = soup.find("div", class_="ui-table__header")
    headers = table_header.find_all("div", "ui-table__headerCell")
    header_data = [header.get_text() for header in headers]
    header_data.pop(-1)
    table_data.append(header_data)
    
    # Extracting body data
    table_body = soup.find("div", class_="ui-table__body")
    rows = table_body.find_all("div", class_="ui-table__row")

    for row in rows:
        rank = row.find("div", class_="tableCellRank")
        team = row.find("a", class_="tableCellParticipant__name")
        cells = row.find_all("span", class_="table__cell--value")

        if cells:
            row_data = [cell.get_text() for cell in cells]
            row_data.insert(0, team.get_text())
            row_data.insert(0, rank.get_text())
            table_data.append(row_data)
    
    table_data_df = pd.DataFrame(table_data)
    file_path = f"./Dane/{number[0]}-{number[1]}.csv"
    table_data_df.to_csv(file_path, index=False, header=False)
    print(f"Data for season {number[0]}-{number[1]} saved to {file_path}")

list_of_seasons = [
    ["2012", "2013"], ["2013", "2014"], ["2014", "2015"],
    ["2015", "2016"], ["2016", "2017"], ["2017", "2018"],
    ["2018", "2019"], ["2019", "2020"], ["2020", "2021"],
    ["2021", "2022"]
]

for season in list_of_seasons:
    get_data(season)