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
    

list_jobs = {'golang','.net','php developer','laravel','java','python','nodejs','reactjs','nextjs','angularjs','fluter','kotlin','vuejs','backend','frontend','mobile','data analyst','data scientist','data engineer','software engineer','software developer','full-stack','programmer','javascript','user interface','user experience','hr officer','accounting officer'}

# list_jobs = {'golang'}

page = 1
data = []

for i in list_jobs:
    search_position = i
    search_position = search_position.lower().replace(' ','+')

# template = 'https://glints.com/id/opportunities/jobs/explore?'
# url_params = 'keyword={}&country=ID&locationName={}' if search_position and location else 'keyword={}&country=ID&locationName=All+Cities%2FProvinces'

    while True:
        # find using listed job #1
        url = 'https://glints.com/id/opportunities/jobs/explore?keyword={}&country=ID&locationName=All+Cities%2FProvinces&page={}'.format(search_position,page)
        # find using category = computer information technology #2
        url = 'https://glints.com/id/job-category/computer-information-technology?page={}'.format(page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='JobCardsc__JobcardContainer-sc-hmqj50-0 iirqVR CompactOpportunityCardsc__CompactJobCardWrapper-sc-dkg8my-2 bMyejJ compact_job_card')

            if len(job_cards) == 0:
                print('No more jobs to fetch')
                break

            for job_card in job_cards:
                job_title = find_tag_value(job_card, 'h3', 'CompactOpportunityCardsc__JobTitle-sc-dkg8my-9 hgMGcy')
                company_name = find_tag_value(job_card, 'a', 'CompactOpportunityCardsc__CompanyLink-sc-dkg8my-10 iTRLWx')
                job_location = find_tag_value(job_card, 'span', 'CardJobLocation__StyledTruncatedLocation-sc-1by41tq-1 kEinQH')
                work_place = find_tag_value(job_card, 'div', 'TagStyle-sc-r1wv7a-4 bJWZOt CompactOpportunityCardTags__Tag-sc-610p59-1 hncMah')
                years_experience = find_tag_value(job_card, 'div', 'TagStyle-sc-r1wv7a-4 bJWZOt CompactOpportunityCardTags__Tag-sc-610p59-1 hncMah')
                more_detail_link = 'https://glints.com'+ job_card.find('a', class_= 'CompactOpportunityCardsc__CardAnchorWrapper-sc-dkg8my-24 knEIai job-search-results_job-card_link').get('href')
                
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
                print(f"Experience: {years_experience}")
                # print(f"Posted Date: {posted_date}")
                # print(f"Salary: {salary_range}")
                
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
            page += 1
        else:
            print(f"Failed to fetch URL: {url}")
            break



df = pd.DataFrame(data)

script_dir = os.path.dirname(os.path.abspath(__file__))
custom_name = f'list_of_jobs_glints_1.csv'
file_path = os.path.join(script_dir, custom_name)
df.to_csv(file_path, index=False, encoding='utf-8')

# # connect to mongodb

# import pymongo
# from pymongo import MongoClient

# # connect to mongodb
 
# client = MongoClient('mongodb://localhost:27017/')
# db = client['jobs']
# collection = db['glints']

# # convert dataframe to dictionary
# data_dict = df.to_dict("records")

# # insert data to mongodb
# collection.insert_many(data_dict)

# # check data in mongodb
# cursor = collection.find({})
# for document in cursor:
#     print(document)






    