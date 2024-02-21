from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import urllib.parse 
import os


def scrape_jobs(position,location):
    position = urllib.parse.quote_plus(position)
    location = urllib.parse.quote_plus(location)
    sequence = 1
    data = []

    while True:
        start_page = 1 + ((sequence - 1) // 10) * 10
        template = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=100&txtKeywords=0DQT0{}0DQT0&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={}&searchBy=0&rdoOperator=OR&txtLocation={}&pDate=I&sequence={}&startPage={}'
        url = template.format(position,position, location, sequence, start_page)
        
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
        print('jobs found', len(jobs),'url',url)

        if not jobs:
            break
        sequence += 1

        for job in jobs:
            try:
                job_role = job.find('h2').text.strip()
            except AttributeError:
                job_role = ''
            try:
                company_name = job.find('h3',class_='joblist-comp-name').text.strip()
            except AttributeError:
                company_name = ''
            try:
                location_company = job.find('span').text.strip()
            except AttributeError:
                location_company = ''
            try:
                posted_date = (job.find('span',class_='sim-posted').span.text).split('Posted')[-1].strip()
            except AttributeError:
                posted_date = ''
            try:
                skill = job.find('span',class_='srp-skills').text.strip()
            except AttributeError:
                skill = ''
            try:
                job_desc = job.find('label', string='Job Description:').find_next_sibling('a').previous_sibling.strip()
            except AttributeError:
                job_desc = '' 
            try:
                more_detail_link = job.header.h2.a['href']
            except AttributeError:
                more_detail_link = ''
            
            extract_date = datetime.today().strftime('%Y-%m-%d')
            
            data.append({'Role':job_role, 'Company Name':company_name, 'Location':location_company, 'Posted Date':posted_date,'Extracted Date':extract_date,'Key Skill': skill,'Job Description':job_desc, 'More Detail':more_detail_link})
          
    df = pd.DataFrame(data)
    

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f'list_of_{position}_timesjobs.csv')

    df.to_csv(file_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    position = 'data analyst'
    location = ''

scrape_jobs(position,location)