from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=software+engineer&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
data = []



jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
for job in jobs:
    job_role = job.find('h2').text.strip()
    company_name = job.find('h3',class_='joblist-comp-name').text.strip()
    location = job.find('span').text.strip()
    posted_date = (job.find('span',class_='sim-posted').span.text).split('Posted')[-1].strip()
    job_desc = job.find('label', string='Job Description:').find_next_sibling('a').previous_sibling.strip()
    data.append({'Role':job_role, 'Company Name':company_name, 'Location':location, 'Posted Date':posted_date, 'Job Description':job_desc})

df = pd.DataFrame(data)

df.to_csv('job_listing_timesjobs.csv', index=False, encoding='utf-8')

