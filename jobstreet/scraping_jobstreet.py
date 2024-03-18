from bs4 import BeautifulSoup
import requests
import pandas as pd
import re, os


# Helper Function
def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, attrs={'data-automation':attribute}).text.strip()
    except AttributeError:
        return None
    
list_jobs = {'golang','.net','php','laravel','java','python','nodejs','reactjs','nextjs','angularjs','fluter','kotlin','vuejs','backend','frontend','mobile','data','software engineer','software developer','full-stack','programmer','javascript'}


# list_jobs = {'golang','.net'}

# list_jobs_2 = {
#     "php" : ["php", "code igniter", "ci", "laravel", "lumen"],
#     "java" : ["java", "springboot"],
#      "python" : ["python", "flask"],
#     "nodejs" : ["node js", "express js", "expressjs", "nodejs", "node", "node-js"],
#     "reactjs" : ["reactjs", "react-js", "react js", "react"],
#     "nextjs" : ["nextjs", "next-js", "next js", "next"],
#     "angularjs" : ["angular", "angularjs"],
#     "fluter" : ["fluter"],
#     "kotlin" : ["kotlin"],
#     "vuejs" : ["vue-js", "vuejs", "vue", "vue js"],
#     "backend" : ["back-end", "backend", "back end", "ruby"],
#     "frontend" : ["front-end", "frontend", "front end", "svelte", "nuxt"],
#     "mobile" : ["mobile", "mobile dev", "mobile apps", "react native", "native", "android", "ios"],
#     "data" : ["data-engineer", "data engineer", "de", "data", "scientist", "analyst", "sql"],
#     "other" : ["software engineer", "software developer", "software", "full-stack", "fullstack", "programmer", "javascript" ]   
# }




    
# search_position = input('Enter Searched Position: ')
# location = input('Enter Location: ')

# search_position = search_position.lower().replace(' ','-')
# location = location.lower().replace(' ','-')

page = 1
data = []

for i in list_jobs:
    search_position = i
    location = ''
    search_position = search_position.lower().replace(' ','-')
    location = location.lower().replace(' ','-')


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
        



            data.append({'Job Title':job_title, 'Company Name':company_name, 'Location':location_city, 'Salary':salary,'Job Classification':job_classification, 'Job Sub Classification':job_sub_classification,'Facility':facility_list, 'Posted Date':posted_date,'Job Type':work_type,'Job Description':job_desc,'More Detail':more_detail_link,'Job ID':job_id})
            
        page += 1

df = pd.DataFrame(data)
script_dir = os.path.dirname(os.path.abspath(__file__))

# save to json file mongodb

custom_name = f'jobs_jobstreet_2.csv'
file_path = os.path.join(script_dir, custom_name)
df.to_csv(file_path, index=False, encoding='utf-8')





    