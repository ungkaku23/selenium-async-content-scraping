from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
browser.get('https://leetcode.com/DBabichev/')
tabs = browser.find_elements(By.CSS_SELECTOR, 'div.cursor-pointer')
solution_links = []
solution_labels = []
for tab in tabs:
    link = tab.find_element(By.CSS_SELECTOR, 'span.whitespace-nowrap')
    if link.text == "Solutions":
        link.click()
        try:
            element = WebDriverWait(browser, 10).until(
                # EC.presence_of_element_located((By.XPATH, "//div[@class='cursor-pointer']"))
                EC.presence_of_element_located((By.XPATH, "//a[contains(@data-tab, 'SOLUTIONS')]"))
            )
            # print(f'founder***:   {element}')
            solution_elements = browser.find_elements(By.XPATH, "//a[contains(@data-tab, 'SOLUTIONS')]")
            print(f"how many : {len(solution_elements)}")
            for solution_element in solution_elements:
                solution_links.append(solution_element.get_attribute("href"))
                label_element = solution_element.find_element(By.CSS_SELECTOR, 'span:nth-child(1)')
                solution_labels.append(label_element.text)
            print(solution_links)
            print(solution_labels)

            df = pd.DataFrame(list(zip(solution_labels, solution_links)), columns=['Label', 'Link'])

            solution_data = df.to_csv('Solutions.csv', index=False)
        except TimeoutException:
            print("Loading took too much time!")

# desc_list =[]
# price_list = []
# shipping_list = []
# i = 0
# while i < 2:
#     try:
#         beach_balls = browser.find_elements_by_css_selector('li.Grid-col.u-size-1-4-l.u-size-3-12-m.u-size-6-12.u-size-1-5-xl')

#         for ball in beach_balls:
#             desc = ball.find_element_by_css_selector('h2.prod-ProductTitle.no-margin.truncated.heading-b').text
#             price = ball.find_element_by_css_selector('div.search-result-productprice.gridview').text.lstrip('Price\n')
#             shipping = ball.find_element_by_css_selector('div.search-result-product-shipping-details.gridview').text

#             desc_list.append(desc)
#             price_list.append(price)
#             shipping_list.append(shipping)

#         browser.find_element_by_css_selector('button.paginator-btn.paginator-btn-next').click()
#         i += 1

#     except exceptions.StaleElementReferenceException:
#          pass

