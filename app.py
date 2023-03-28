from flask import Flask, render_template, request
import selenium
from selenium.webdriver import PhantomJS
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
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
import os

app = Flask(__name__)

class ReshipScraper:
    def __init__(self):
        self.driver = PhantomJS()
        self.driver.get("about:blank")
        self.driver.delete_all_cookies()

    def signup(self, name, email, password, phone, country):
        wait = WebDriverWait(self.driver, 20)
        self.driver.delete_all_cookies()
        try:
            # Extract the required information from the form data
            reship_email = 'chungtin+{}@linkdayne.com'.format(name)

            # Use Selenium to interact with the Reship signup page
            self.driver.get("https://ship.reship.com/register/free")
            self.driver.execute_script('localStorage.clear();')
            time.sleep(1)
            if ' Logout' in self.driver.page_source:
                self.driver.delete_all_cookies()
                time.sleep(5)
                self.driver.get("https://ship.reship.com/register/free")
                self.driver.execute_script('localStorage.clear();')

            name_field = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/input')))
            name_field.send_keys(name)
            email_field = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/input')))
            email_field.send_keys(reship_email)
            phone_field = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[5]/div/input')))
            phone_field.send_keys(phone)
            country_field = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[4]/select')))
            country_field.send_keys(country)
            

            verify_button = self.driver.find_element_by_css_selector("div.btn.btn-primary")
            verify_button.click()
            time.sleep(4)
            
            # Replace with the email address you want to fetch messages from
            user_id = 'chungtin@linkdayne.com'
            
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                service = build('gmail', 'v1', credentials=creds)
                results = service.users().messages().list(userId=user_id).execute()
                messages = results.get('messages', [])

                if messages:
                    for message in messages:
                        msg = service.users().messages().get(userId='me', id=message['id']).execute()
                        var = msg['snippet'].strip()[-6:]
                        print(var)
                        code_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[6]/input')))
                        code_input_has_value = False
                        while not code_input_has_value:
                            code_input.send_keys(var)
                            code_input_has_value = wait.until(EC.text_to_be_present_in_element_value((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[6]/input'), var))
                        next_button = self.driver.find_element_by_css_selector("div.btn.btn-primary")
                        next_button.click()
                        time.sleep(1)

                        password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/input')))
                        confirm_password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/input')))

                        
                        password_input.send_keys(password)
                        confirm_password_input.send_keys(password)
                        
                        next_button = self.driver.find_element_by_css_selector("div.btn.btn-primary")
                        next_button.click()
                        time.sleep(3)
                        break
            page = self.driver.page_source
            self.driver.delete_all_cookies()
            self.driver.quit
            return page
        except TimeoutException:
            page = self.driver.page_source
            self.driver.delete_all_cookies()
            self.driver.quit
            return page
                

    
reship_scraper = ReshipScraper()

@app.route('/signup123')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us.html')
def about():
    return render_template('about-us.html')

@app.route('/tracking.html')
def tracking():
    return render_template('tracking.html')

@app.route('/pricing-plans.html')
def pricing():
    return render_template('pricing-plans.html')

@app.route('/contact-us.html')
def contact():
    return render_template('contact-us.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/get-quote.html')
def quote():
    return render_template('get-quote.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form
    print(data)
    # do something with the webhook data
    return '', 200

@app.route('/signup', methods=['POST'])
def signup():
    # Get the form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    country = request.form['rcrs-country']

    # Signup using ReshipScraper
    result = reship_scraper.signup(name, email, password, phone, country)

    return result

@app.route('/shipEstimate', methods=['POST'])
def ship_estimate():
    # Get the request data
    data = request.data
    headers = request.headers

    # Make a copy of the request data
    copied_data = data

    # Post the copied request to another endpoint
    response = requests.post('https://api-customer.reship.com/shipEstimate', data=copied_data, headers=headers)

    # Return the response from the other endpoint
    return response.content, response.status_code

if __name__ == '__main__':
    app.run(debug=True)