
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import *

def attach_driver(debug):
    options = webdriver.ChromeOptions()
    options.debugger_address = debug
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)
