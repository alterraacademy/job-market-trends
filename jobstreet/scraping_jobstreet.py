from bs4 import BeautifulSoup
import requests
import pandas as pd
import re, os, time

# Helper Function
def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, attrs={'data-automation':attribute}).text.strip()
    except AttributeError:
        return None

def save_data_to_csv(data, current_date):
    df = pd.DataFrame(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_name = 'output_dataset'
    new_folder_path = os.path.join(script_dir, new_folder_name)
    custom_name = f'{current_date}.csv'
    file_path = os.path.join(new_folder_path, custom_name)

    # file_path = os.path.join(script_dir, custom_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        df.to_csv(file_path, index=False)
    else:
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)

    while os.path.exists(file_path):
        custom_name = f'{current_date}_{counter}.csv'
        file_path = os.path.join(script_dir, custom_name)
        counter += 1
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Data Collected")
    
# # list_jobs = {'golang','.net','php','laravel','java','python','nodejs','reactjs','nextjs','angularjs','fluter','kotlin','vuejs','backend','frontend','mobile','data','software engineer','software developer','full-stack','programmer','javascript','hr officer','accounting officer'}
# list_jobs = {'golang','.net'}
page = 1
data = []

# for i in list_jobs:
#     search_position = i
#     location = ''
#     search_position = search_position.lower().replace(' ','-')
#     location = location.lower().replace(' ','-')

# search_position = input('Enter the job position you are searching for: ')
# location = input('Enter the location you are searching for: ')


while True:
    
    # base_url = 'https://www.jobstreet.co.id/id/'
    # url_params = '{}-jobs/in-{}' if search_position and location else '{}-jobs' if search_position else 'jobs-in-{}' if location else 'jobs'

    # url = base_url + url_params.format(search_position, location) + '?page={}'.format(page) if search_position or location else base_url + 'jobs?page={}'.format(page)
    url = 'https://www.jobstreet.co.id/id/jobs?classification=6261%2C1223%2C6281&page={}&subclassification=6222%2C6223%2C6283%2C6285%2C6286%2C6287%2C6289%2C6290%2C6298%2C6301%2C6302'.format(page)
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, 'lxml')
    job_cards = soup.find_all('article',attrs={'data-card-type':'JobCard'})

    current_date = pd.Timestamp.now().strftime('%Y-%m-%d')

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

        base_detail_url = 'https://www.jobstreet.co.id/id/job/{}?type=standard&ref=search-standalone'
        r_detail = requests.get(base_detail_url.format(job_id))
        soup = BeautifulSoup(r_detail.content, 'lxml')
        work_type = find_tag_value(soup,'span','job-detail-work-type')
        job_desc = find_tag_value(soup, 'div', 'jobAdDetails')
    
        data.append({'job_title':job_title, 'company_name':company_name, 'location':location_city, 'salary':salary,'job_classification':job_classification, 'job_sub_Classification':job_sub_classification,'facility':facility_list, 'posted Date':posted_date,'work_type':work_type,'job_description':job_desc,'more_detail_link':more_detail_link,'job_id':job_id})
        

    page += 1
save_data_to_csv(data,current_date)
# df = pd.DataFrame(data)
# script_dir = os.path.dirname(os.path.abspath(__file__))
# current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
# new_folder_path = os.path.join(script_dir, current_date)
# file_path = os.path.join(new_folder_path, current_date)

# if data:
#     # Convert the collected data into a DataFrame
#     df = pd.DataFrame(data)
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     custom_name = f'{current_date}.csv'  # Name of the CSV file based on the search_position
#     file_path = os.path.join(script_dir, custom_name)
#     df.to_csv(file_path, index=False, encoding='utf-8')  # Save to CSV
#     print(f"Data Collected")

# page = 1


# df = pd.DataFrame(data)
# script_dir = os.path.dirname(os.path.abspath(__file__))

# save to json file mongodb

# file_path = os.path.join(script_dir, custom_name)
# df.to_csv(file_path, index=False, encoding='utf-8')





    