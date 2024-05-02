from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pandas as pd 
import os 



# searched_position = input('Enter search position here: ')
data = []
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/jobs/search/?keywords=frontend%20developer&origin=SUGGESTION&position=1&pageNum=0')

try:
    

    ul = driver.find_elements(By.CLASS_NAME,"jobs-search__results-list")

    for ul_element in ul:
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        # print('print_li')
        for li in li_elements:
            # card = li.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/ul/li[1]/div').text
            # card.click()

            # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "details-pane__content.details-pane__content--show")))

            job_title = li.find_element(By.CLASS_NAME, 'base-search-card__title').text
            company_name = li.find_element(By.CSS_SELECTOR, '.hidden-nested-link').text.strip()
            location = li.find_element(By.CSS_SELECTOR,'.job-search-card__location').text.strip()
            current_date = pd.Timestamp.now().strftime('%Y-%m-%d')

            data.append({'job_title':job_title,'company_name':company_name,'location':location,'scrapped_date':current_date})
            # details = li.find_element

            print(job_title,company_name,location)
    
    driver.implicitly_wait(5)


except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()

if data:
    # Convert the collected data into a DataFrame
    df = pd.DataFrame(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_name = f'{current_date}.csv'  # Name of the CSV file based on the search_position
    file_path = os.path.join(script_dir, custom_name)
    df.to_csv(file_path, index=False, encoding='utf-8')  # Save to CSV
    print(f"Data Collected")