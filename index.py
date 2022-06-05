from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import os

def load_more_data(page):
    solution_links = []
    solution_labels = []
    print(f"page {page}")
    try:
        wait = WebDriverWait(browser, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex w-full items-center justify-center mt-4')]")))
        load_more_btn = browser.find_element(By.XPATH, "//div[contains(@class, 'flex w-full items-center justify-center mt-4')]")
        load_more_btn.click()
        time.sleep(3)
        page += 1
        load_more_data(page)
    except TimeoutException:
        print("Not found load more button")
        
        solution_elements = browser.find_elements(By.XPATH, "//a[contains(@data-tab, 'SOLUTIONS')]")
        size = len(solution_elements)
        if len(solution_elements) > 500:
            size = 500

        for x in range(size):
            # solution_links.append(solution_elements[x].get_attribute("href"))
            label_element = solution_elements[x].find_element(By.CSS_SELECTOR, 'span:nth-child(1)')
            solution_labels.append(label_element.text)
            text_file = open(f"./output/{label_element.text}.txt", "w")
            n = text_file.write(solution_elements[x].get_attribute("href"))
            text_file.close()

def start_grab(logged_browser):
    tabs = logged_browser.find_elements(By.CSS_SELECTOR, 'div.cursor-pointer')

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    for tab in tabs:
        link = tab.find_element(By.CSS_SELECTOR, 'span.whitespace-nowrap')
        if link.text == "Solutions":
            link.click()
            try:
                element = WebDriverWait(logged_browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@data-tab, 'SOLUTIONS')]"))
                )

                load_more_data(1)
            except TimeoutException:
                print("Loading took too much time!")


browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
browser.get('https://leetcode.com/accounts/login/?next=/DBabichev/')
try:
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@data-cy, 'username')]")))
    print("Found form")
    
    username = browser.find_element(By.XPATH, "//input[contains(@data-cy, 'username')]")
    password = browser.find_element(By.XPATH, "//input[contains(@data-cy, 'password')]")

    username.send_keys("test23216")
    password.send_keys("test23pw")

    browser.find_element(By.XPATH, "//button[contains(@data-cy, 'sign-in-btn')]").click()
    time.sleep(3)
    print("logged in")
    start_grab(browser)
except TimeoutException:
    print("Not found form")

