from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Helper Function
def find_tag_value(soup, tag, class_name):
    try:
        return soup.find(tag, class_=(class_name)).text.strip()
    except AttributeError:
        return None
    
def find_tag_attr(job_card, attr):
    try:
        return job_card.find('div', {'data-gtm-job-' + attr: True})['data-gtm-job-' + attr]
    except (AttributeError, KeyError):
        return None
    

# list_jobs = {'golang','.net','php','laravel','java','python','nodejs','reactjs','nextjs','angularjs','fluter','kotlin','vuejs','backend','frontend','mobile','data','software engineer','software developer','full-stack','programmer','javascript','hr officer','accounting officer'}

list_jobs = {'golang'}

# page = 1
# data = []

# for i in list_jobs:
#     search_position = i
#     location = ''
#     search_position = search_position.lower().replace(' ','+')
#     location = location.lower().replace(' ','+')

# template = 'https://glints.com/id/opportunities/jobs/explore?'
# url_params = 'keyword={}&country=ID&locationName={}' if search_position and location else 'keyword={}&country=ID&locationName=All+Cities%2FProvinces'


data = []
url = 'https://glints.com/id/opportunities/jobs/explore?keyword={}&country=ID&locationName=All+Cities%2FProvinces'.format(list_jobs)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    job_cards = soup.find_all('div', class_='JobCardsc__JobcardContainer-sc-hmqj50-0 iirqVR CompactOpportunityCardsc__CompactJobCardWrapper-sc-dkg8my-2 bMyejJ compact_job_card')

    for job_card in job_cards:
        job_title = find_tag_value(job_card, 'h3', 'CompactOpportunityCardsc__JobTitle-sc-dkg8my-9 hgMGcy')
        company_name = find_tag_value(job_card, 'a', 'CompactOpportunityCardsc__CompanyLink-sc-dkg8my-10 iTRLWx')
        job_location = find_tag_value(job_card, 'span', 'CardJobLocation__StyledTruncatedLocation-sc-1by41tq-1 kEinQH')
        work_place = find_tag_value(job_card, 'div', 'TagStyle-sc-r1wv7a-4 bJWZOt CompactOpportunityCardTags__Tag-sc-610p59-1 hncMah')
        # years_experience = find_tag_value(job_card, 'div', 'TagStyle__TagContentWrapper-sc-r1wv7a-1 koGVuk')
        more_detail_link = 'https://glints.com'+ job_card.find('a', class_= 'CompactOpportunityCardsc__CardAnchorWrapper-sc-dkg8my-24 knEIai job-search-results_job-card_link').get('href')
        
        posted_date = find_tag_value(job_card, 'div', 'CompactOpportunityCardsc__OpportunityFooter-sc-dkg8my-19 hwYSIu')
        current_date = pd.Timestamp.now().strftime('%Y-%m-%d')

        if 'hari' in posted_date:
            days = int(posted_date[0])
            posted_date = (pd.Timestamp.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')
        elif 'Kemarin' in posted_date:
            posted_date = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        

        salary_range = find_tag_value(job_card, 'span', 'CompactOpportunityCardsc__NotDisclosedMessage-sc-dkg8my-23 hivaYx')
        if salary_range:
            salary_range = 'Not Written'
        else:
            salary_range = find_tag_value(job_card, 'span', 'CompactOpportunityCardsc__SalaryWrapper-sc-dkg8my-29 gfPeyg')
        
        skill = find_tag_attr(job_card, 'card-info').replace('experience,logo,','')
        job_id = find_tag_attr(job_card, 'id')
        work_type = find_tag_attr(job_card, 'type')
        category = find_tag_attr(job_card, 'category')
        sub_category = find_tag_attr(job_card, 'sub-category')
        role = find_tag_attr(job_card, 'role')

        print(f"Job Title: {job_title}")
        print(f"Company Name: {company_name}")

        print(f"Posted Date: {posted_date}")
        print(f"Salary: {salary_range}")
        
        data.append({
            'job_title': job_title,
            'company_name': company_name,
            'job_location': job_location,
            'work_place': work_place,
            'salary_range': salary_range,
            'more_detail_link': more_detail_link,
            'job_id': job_id,
            'work_type': work_type,
            'category': category,
            'sub_category': sub_category,
            'role': role
        })
        
else:
    print(f"Failed to fetch URL: {url}")



df = pd.DataFrame(data)
# script_dir = os.path.dirname(os.path.abspath(__file__))
# custom_name = f'list_of_jobs_glints.csv'
# file_path = os.path.join(script_dir, custom_name)
# df.to_csv(file_path, index=False, encoding='utf-8')





    