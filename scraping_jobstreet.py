from bs4 import BeautifulSoup
import requests
import pandas as pd
import re, os

search_position = 'programmer'
location = 'surabaya'
search_position = search_position.replace(' ','-')
location = location.replace(' ','-')

def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, attrs={'data-automation':attribute}).text.strip()
    except AttributeError:
        return None
    

page = 1
data = []
while True:
    if search_position and location:
        r = requests.get('https://www.jobstreet.co.id/id/{}-jobs/in-{}?page={}'.format(search_position, location, page))
        soup = BeautifulSoup(r.content, 'lxml')
        job_cards = soup.find_all('article',attrs={'data-card-type':'JobCard'})

    # elif location is null  but search_position is not null
    elif search_position and not location:
        r = requests.get('https://www.jobstreet.co.id/id/{}-jobs?page={}'.format(search_position, page))
        soup = BeautifulSoup(r.content, 'lxml')
        job_cards = soup.find_all('article',attrs={'data-card-type':'JobCard'})
    
    elif not search_position and location:
        r = requests.get('https://www.jobstreet.co.id/id/jobs-in-{}?page={}'.format(location, page))
        soup = BeautifulSoup(r.content, 'lxml')
        job_cards = soup.find_all('article',attrs={'data-card-type':'JobCard'})
    
    else:
        r = requests.get('https://www.jobstreet.co.id/id/jobs?page={}'.format(page))
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
        
        job_desc = find_tag_value(job_card, 'span', 'jobShortDescription')

        posted_date = find_tag_value(job_card, 'span', 'jobListingDate')
        
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
        
        # job_detail_request = requests.get('https://www.jobstreet.co.id/id/{}-jobs/in-{}?jobId={}&type=standout'.format(search, location, job_id))
        # soup_job_detail_request = BeautifulSoup(job_detail_request.content, 'lxml')
        # job_cards = soup_job_detail_request.find_all('article',attrs={'data-card-type':'JobCard'}) 

        data.append({'Job Title':job_title, 'Company Name':company_name, 'Location':location_city, 'Salary':salary, 'Job Classification':job_classification, 'Job Sub Classification':job_sub_classification, 'Job Description':job_desc, 'Facility':facility_list, 'Posted Date':posted_date})
        
    page += 1

df = pd.DataFrame(data)
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'jobstreet.csv')

df.to_csv(file_path, index=False, encoding='utf-8')


    