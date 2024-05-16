from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import urllib.parse
import re, json, os

def save_data_to_csv(data):
    df = pd.DataFrame(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_name = 'output_dataset'
    new_folder_path = os.path.join(script_dir, new_folder_name)
    current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    
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
    

def convert_columns_data_type(df, cols, datatype):
    for col in cols:
        df[col] = df[col].astype(datatype)
        
def scrape_job_details(page_source):
    content = BeautifulSoup(page_source, 'lxml')
    # print(content)
    jobs_list = []    
    for post in content.select('.job_seen_beacon'):

        data = {
            "job_title": post.find('span', id=lambda x: x and x.startswith('jobTitle')).text,
            "company": post.find('span', class_='css-92r8pb').text,
            "location": post.find('div', class_='css-1p0sjhy').text,
            "posted_date":  post.find('span', attrs={'data-testid': 'myJobsStateDate'}).text,
            "more_detail_link" : post.find('a',class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href'),
            # "job_description": post.find('div', class_='css-9446fg').text,
            # "job_type": post.find('span', class_='css-12bzcbs').text,
            "scrapped_date": pd.to_datetime('today').strftime('%Y-%m-%d')
        }

        try: data["rating"] = post.find('span', attrs={'data-testid': 'holistic-rating'}).text
        except: data["rating"] = 0
        jobs_list.append(data)
        # print(data)

    # df = pd.DataFrame(jobs_list)
    # if 'rating' in df.columns:
    #     convert_columns_data_type(df, ['rating'], np.float32) # Convert rating to float

new_results = []
job_search = input('Enter searched position: ')
job_query = urllib.parse.quote(job_search)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for i in range(10):
    url = 'https://id.indeed.com/jobs?q={}&start={}&l=&from=searchOnHP'.format(job_query,10 + i*10)
    response = requests.get(url, headers=headers)
    result = scrape_job_details(response.content)
    new_results.append(result)
    print(new_results)
    # save_data_to_csv(new_results)

# combined_data = pd.concat(new_results, ignore_index=True)



