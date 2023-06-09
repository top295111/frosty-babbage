
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
from flask import request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/shipEstimate', methods=['POST'])
def ship_estimate():

    len = request.json['len']
    width = request.json['width']
    height = request.json['height']
    weight = request.json['weight']
    city = request.json['city']
    countryCode = request.json['countryCode']
    postalCode = request.json['postalCode']
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 20)

    driver.get("https://ship.reship.com/calculator")
    driver.execute_script('localStorage.clear();')
    time.sleep(1)
   
    width_field = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/input')
    width_field.send_keys(width)
    height_field = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div[3]/input')
    height_field.send_keys(height)
    
    # page = driver.find_element_by_css_selector("div.ship-quotes").get_attribute("outerHTML")
    page = driver.page_source
    driver.delete_all_cookies()
    driver.quit
    return page


if __name__ == '__main__':
    app.run(debug=True)