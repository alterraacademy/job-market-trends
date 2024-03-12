from bs4 import BeautifulSoup
import requests
import pandas as pd
import re, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Helper Function
def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, attrs={'data-automation':attribute}).text.strip()
    except AttributeError:
        return None
    


# job_title = ['business intelligence']


# for i in job_title:
#     search_position = i
#     location = ''
#     search_position = search_position.lower().replace(' ','-')
#     location = location.lower().replace(' ','-')


    
search_position = input('Enter Searched Position: ')
location = input('Enter Location: ')

search_position = search_position.lower().replace(' ','-')
location = location.lower().replace(' ','-')


page = 1
data = []
while True:
    base_url = 'https://www.jobstreet.co.id/id/'
    url_params = '{}-jobs/in-{}' if search_position and location else '{}-jobs' if search_position else 'jobs-in-{}' if location else 'jobs'

    url = base_url + url_params.format(search_position, location) + '?page={}'.format(page) if search_position or location else base_url + 'jobs?page={}'.format(page)
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, 'lxml')
    job_cards = soup.find_all('article',attrs={'data-card-type':'JobCard'})

        
    if len(job_cards) == 0:
        print('No More Jobs')
        break
    print('page',page,'jobs found', len(job_cards))

    for job_card in job_cards:
    
        job_title = find_tag_value(job_card, 'a', 'jobTitle')
        
        company_name = find_tag_value(job_card, 'a', 'jobCompany')
        
        location_city = find_tag_value(job_card, 'a', 'jobLocation')
        
        salary = find_tag_value(job_card, 'span', 'jobSalary')
        if salary:
            salary = salary.replace(u'\xa0', u'')

        job_classification = find_tag_value(job_card, 'a', 'jobClassification')
            #remove () from job_classification
        if job_classification:
            job_classification = re.sub(r'[()]', '', job_classification)

        job_sub_classification = find_tag_value(job_card, 'a', 'jobSubClassification')
        
        job_short_desc = find_tag_value(job_card, 'span', 'jobShortDescription') 

        posted_date = find_tag_value(job_card, 'span', 'jobListingDate')
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        
        if 'hari' in posted_date:
            days = int(posted_date[0])
            posted_date = (pd.Timestamp.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')
        else:
            posted_date = current_date
        
        facility = job_card.find('ul',class_='y735df0 y735df3 _1akoxc50 _1akoxc54')
        if facility is not None:
            facility = facility.find_all('li')
            facility_list = [item.text.strip() for item in facility]
            facility_list = ', '.join(facility_list)
        else:
            facility_list = ''
        
        more_detail_link = job_card.find('a', attrs={'data-automation':'job-list-view-job-link'})
        if more_detail_link:
            more_detail_link = 'https://www.jobstreet.co.id'+ (more_detail_link.get('href'))
        
        job_id = job_card['data-job-id']

        detail_url_params = 'jobs/in-{}?jobId={}&type=standout' 
        
        job_detail_section = soup.find('div', attrs={'data-sticky':'job-details-page'})
        # Getting Detail Job Page

        
        job_detail_type = job_detail_section.find('span', attrs={'data-automation':'job-detail-work-type'}).text.strip()

        job_detail_desc = job_detail_section.find('div', attrs={'data-automation':'jobAdDetails'}).text.strip()

        # driver = webdriver.Chrome()
        # job_detail_url = 'https://www.jobstreet.co.id/id/{}-jobs/in-{}?jobId={}&type=standout'.format(search_position, location, job_id)
        # driver.get(job_detail_url)

        # job_details_section = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[data-automation="jobDetailsPage"]')))
        # soup_job_detail_request = BeautifulSoup(driver.page_source, 'lxml')

        # job_detail_page = soup_job_detail_request.find('div', attrs={'data-automation':'jobDetailsPage'})

        # work_type = find_tag_value(job_detail_page, 'sdpan', 'job-detail-work-type')

        # job_desc = find_tag_value(job_detail_page, 'div', 'jobAdDetails')
        
        # driver.quit()
        

        data.append({'Job Title':job_title, 'Company Name':company_name, 'Location':location_city, 'Salary':salary, 'Job Classification':job_classification, 'Job Sub Classification':job_sub_classification, 'Job Description':job_short_desc, 'Facility':facility_list, 'Posted Date':posted_date,'More Detail':more_detail_link})
        
    page += 1

df = pd.DataFrame(data)
script_dir = os.path.dirname(os.path.abspath(__file__))
custom_name = f'list_of_jobs_jobstreet.csv'
file_path = os.path.join(script_dir, custom_name)
df.to_csv(file_path, index=False, encoding='utf-8')





    