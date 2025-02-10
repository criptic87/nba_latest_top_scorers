from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_top_scorers():

    service = Service(r"C:\webdriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.nba.com/stats")

    wait = WebDriverWait(driver, 10)  
    try:
        table_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "LeaderBoardPlayerCard_lbpcTable__q3iZD"))
        )
    except Exception as e:
        print("Error: Table did not load within the time limit.")
        driver.quit()
        return []

    html = table_element.get_attribute("outerHTML")

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.find_all("tr")[0:]

    top_scorers = []

    for row in rows[:5]:
        columns = row.find_all("td")
        player_name = columns[1].text.strip()
        points = columns[2].text.strip()
        top_scorers.append((player_name, points))
    
    driver.quit()
    return top_scorers

@app.route('/')

def index():
    scorers = get_top_scorers()
    return render_template('index.html', scorers=scorers)

if __name__ == '__main__':
    app.run(debug=True)

