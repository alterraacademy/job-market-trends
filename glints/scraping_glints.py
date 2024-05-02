from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re
import pymongo
from pymongo import MongoClient
import csv

# Helper Function
def find_tag_value(soup, tag, class_name, index=None):
    try:
        elements = soup.find_all(tag, class_=class_name)
        if index is None:
            return elements[0].text.strip() if elements else None
        elif len(elements) > index:
            return elements[index].text.strip()
        else:
            return None
    except AttributeError:
        return None

    
def find_tag_attr(job_card, attr):
    try:
        return job_card.find('div', {'data-gtm-job-' + attr: True})['data-gtm-job-' + attr]
    except (AttributeError, KeyError):
        return None
    
# Initialization
data = []
page = 1

searched_position = input('Enter the job you want to search: ')
searched_position = searched_position.replace(' ', '+')

# Scraping
while True:
    # url = 'https://glints.com/id/job-category/computer-information-technology?page={}'.format(page)
    url = 'https://glints.com/id/opportunities/jobs/explore?keyword={}&country=ID&locationName=All+Cities%2FProvinces&page={}'.format(searched_position, page)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    job_cards = soup.find_all('div', class_='JobCardsc__JobcardContainer-sc-hmqj50-0 iirqVR CompactOpportunityCardsc__CompactJobCardWrapper-sc-dkg8my-2 bMyejJ compact_job_card')
    if len(job_cards) == 0:
        print('No More Jobs')
        break
    print('page',page,'jobs found', len(job_cards))
            
    for job_card in job_cards:
        job_title = find_tag_value(job_card, 'h3', 'CompactOpportunityCardsc__JobTitle-sc-dkg8my-9 hgMGcy')
        company_name = find_tag_value(job_card, 'a', 'CompactOpportunityCardsc__CompanyLink-sc-dkg8my-10 iTRLWx')
        job_location = find_tag_value(job_card, 'span', 'CardJobLocation__StyledTruncatedLocation-sc-1by41tq-1 kEinQH')
        work_place = find_tag_value(job_card, 'div', 'TagStyle-sc-r1wv7a-4 bJWZOt CompactOpportunityCardTags__Tag-sc-610p59-1 hncMah')
        job_tags = [find_tag_value(job_card, 'div', 'TagStyle-sc-r1wv7a-4 bJWZOt CompactOpportunityCardTags__Tag-sc-610p59-1 hncMah', index=i) for i in range(4)]
        job_tag_values = [tag for tag in job_tags]
        years_experience = job_tag_values[2]
        min_education = job_tag_values[3]
        
        salary_range = find_tag_value(job_card, 'span', 'CompactOpportunityCardsc__NotDisclosedMessage-sc-dkg8my-23 hivaYx')
        if salary_range:
            salary_range = 'Not Written'
        else:
            salary_range = find_tag_value(job_card, 'span', 'CompactOpportunityCardsc__SalaryWrapper-sc-dkg8my-29 gfPeyg')
        
        skill = find_tag_attr(job_card, 'card-info')
        job_id = find_tag_attr(job_card, 'id')
        work_type = find_tag_attr(job_card, 'type')
        category = find_tag_attr(job_card, 'category')
        sub_category = find_tag_attr(job_card, 'sub-category')
        role = find_tag_attr(job_card, 'role')

        more_detail_link = 'https://glints.com'+ job_card.find('a', class_= 'CompactOpportunityCardsc__CardAnchorWrapper-sc-dkg8my-24 knEIai job-search-results_job-card_link').get('href')
        response_detail = requests.get(more_detail_link, headers=headers)
        soup_detail = BeautifulSoup(response_detail.content, 'html.parser')
        job_description = find_tag_value(soup_detail,'div','JobDescriptionsc__DescriptionContainer-sc-22zrgx-2 jCwTA-d')
        scrapped_date = pd.Timestamp.now().strftime('%Y-%m-%d')

        data.append({
            'job_title': job_title,
            'company_name': company_name,
            'job_location': job_location,
            'work_place': work_place,
            'salary_range': salary_range,
            'skill': skill,
            'more_detail_link': more_detail_link,
            'job_id': job_id,
            'work_type': work_type,
            'workplace': work_place,
            'years_experience': years_experience,
            'min_education': min_education,
            'category': category,
            'sub_category': sub_category,
            'role': role,
            'scrapped_date': scrapped_date,
        })
        
    page += 1
    
# Stop the loop
print('Total Jobs:', len(data))
df = pd.DataFrame(data)

script_dir = os.path.dirname(os.path.abspath(__file__))
custom_name = f'{scrapped_date}.csv'  # Name of the CSV file based on the search_position
file_path = os.path.join(script_dir, custom_name)
df.to_csv(file_path, index=False, encoding='utf-8')  # Save to CSV
print(f"Data Collected")

# # Connect to MongoDB
# client = MongoClient('localhost', 27017)
# db = client['job']
# collection = db['glints']

# with open(file_path, 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         # check if the job already exists in the collection
#         if collection.find_one({'job_id': row['job_id']}):
#             print('Job already exists')
#         else:
#             collection.insert_one(row)

# for each job_description, find what sub_category it belongs to


    