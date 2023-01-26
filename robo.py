# %%
import pandas as pd
import numpy as np
import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
# Configuring the driver to sign in properly so that it can run as fast as possible

opt = webdriver.FirefoxOptions()
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")
opt.add_argument("--disable-dev-shm-usage")
opt.add_argument("--disable-extensions")
opt.add_argument("--disable-browser-side-navigation")
opt.add_argument("--enable-javascript")
opt.add_argument("--disable-infobars")
opt.add_argument("--window-size=1366,768")

# %%
# This actually instantiates the driver and opens the sign-in page for Geocaching
driver = webdriver.Firefox(options=opt)

driver.get('https://www.geocaching.com/account/signin?returnUrl=%2fplay')


# %%
# Reading in my secrets

with open("secrets.txt") as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
    print(f"USERNAME={username}, PASSWORD={password}")

# %%
# locate the username and password fields and enter the login credentials *CREDENTIALS MUST BE PASSED AS STRINGS*
username_field = driver.find_elements(By.ID,"UsernameOrEmail")
password_field = driver.find_elements(By.ID,"Password")

username_field[0].send_keys(str(username))
password_field[0].send_keys(str(password))

# %%
# locate the login button and click it
login_button = driver.find_element(By.ID, "SignIn")

login_button.click()

# wait for the login to complete. Will wait until the URL changes
wait = WebDriverWait(driver, 10)
wait.until(EC.url_changes("https://www.geocaching.com/play"))

# %%
# send a GET request to the API with the logged in cookies
session = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    session.cookies.update({cookie["name"]: cookie["value"]})

api_response = session.get("https://www.geocaching.com/api/proxy/web/search/v2?skip=0&take=50&asc=true&sort=distance&properties=callernote&rad=16093.44&origin=40.2139%2C-111.6336&dorigin=34.03557%2C-84.20132")

# %%
# read the response into a pandas df
df = pd.DataFrame(api_response.json())

# %%
print(df)

# %%

# close the browser
driver.quit()


