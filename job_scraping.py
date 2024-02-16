from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_url(position,location):
    urls = []
    for sequence in range(1, 11):
        start_page = 1 + ((sequence - 1) // 10) * 10
        template = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=100&txtKeywords={}&postWeek=30&searchType=personalizedSearch&actualTxtKeywords={}&searchBy=0&rdoOperator=OR&txtLocation={}&pDate=I&sequence={}&startPage={}'
        url = template.format(position,position, location, sequence, start_page)
        urls.append(url)
    return urls

def scrape_jobs(position,location):
    urls = get_url(position, location)
    data = []
    for url in urls:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
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
                location = job.find('span').text.strip()
            except AttributeError:
                location = ''
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
            
            data.append({'Role':job_role, 'Company Name':company_name, 'Location':location, 'Posted Date':posted_date, 'Key Skill': skill,'Job Description':job_desc, 'More Detail':more_detail_link})
    df = pd.DataFrame(data)
    df.to_csv('list_of_job_timesjobs.csv', index=False, encoding='utf-8')

# create main
if __name__ == '__main__':
    # position = input('Enter the position you are looking for: ')
    # location = input('Enter the location you are looking for: ')
    position = 'software engineer'
    location = 'bangalore'
    scrape_jobs(position, location)


# html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=software+engineer&txtLocation=').text
# soup = BeautifulSoup(html_text, 'lxml')
# data = []

# jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
# for job in jobs:
#     job_role = job.find('h2').text.strip()
#     company_name = job.find('h3',class_='joblist-comp-name').text.strip()
#     location = job.find('span').text.strip()
#     posted_date = (job.find('span',class_='sim-posted').span.text).split('Posted')[-1].strip()
#     job_desc = job.find('label', string='Job Description:').find_next_sibling('a').previous_sibling.strip()
#     data.append({'Role':job_role, 'Company Name':company_name, 'Location':location, 'Posted Date':posted_date, 'Job Description':job_desc})

# df = pd.DataFrame(data)

# df.to_csv('job_listing_timesjobs.csv', index=False, encoding='utf-8')

