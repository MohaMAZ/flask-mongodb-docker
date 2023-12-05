from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time, os,sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Create a new instance of the Chrome webdriver
driver = webdriver.Chrome('C:/Users/MOHAMAZ/chromedriver.exe')

def login():

    #Access the login page
    driver.get('https://twitter.com/i/flow/login')

    email = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    #Entrer l'émail'
    
    email.send_keys(os.environ.get('EMAIL'))
    email.send_keys(Keys.ENTER)

    time.sleep(5)

    #Sometimes twitter asks for username when it suspects unusual login
    
    #Entrer le username
    username = driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"]')
    username.send_keys(os.environ.get('USR'))
    username.send_keys(Keys.ENTER)

    time.sleep(5)

    #Entrer le password
    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(os.environ.get('PASSWORD'))
    password.send_keys(Keys.ENTER)

    time.sleep(5)

def get_posts(hashtag):

    #Chercher le hashtag harassment
    driver.get('https://twitter.com/search?q=%23'+ hashtag + '&src=typeahead_click')


    elements = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
    elements_ = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')

    time.sleep(5)

    tweets = []
    for element in elements_:
        tweets.append(element.text)
    df = pd.DataFrame(tweets, columns=["tweets"])

    df.to_csv("tweets.csv", index=False, encoding='utf-8')

if __name__ == '__main__':
    login()
    get_posts('harassment')


# Close the browser window
driver.quit()