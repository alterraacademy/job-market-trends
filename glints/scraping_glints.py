from bs4 import BeautifulSoup
import requests
import pandas as pd
import re, os

num_data = 5
page_number = 1
job_data = []

def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, class_=attribute).text.strip()
    except AttributeError:
        return None

while len(job_data) < num_data:
    # Build the URL with the current page number
    url = f"https://glints.com/id/lowongan-kerja?page={page_number}"
    
    # Make a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Perform your scraping code here for the current page
    results = soup.find(id="__next")
    job_elements = results.find_all("div", class_="JobCardsc__JobcardContainer-sc-hmqj50-0 iirqVR CompactOpportunityCardsc__CompactJobCardWrapper-sc-dkg8my-2 bMyejJ compact_job_card")
    print(job_elements)
    
    # for job_element in job_elements:
    #     job_title = find_tag_value(job_element, "h3", "CompactOpportunityCardsc__JobTitle-sc-dkg8my-9 hgMGcy")
    #     company = find_tag_value(job_element, "span", "CompactOpportunityCardsc__CompanyLink-sc-dkg8my-10 iTRLWx")
    #     location = find_tag_value(job_element, "span", "CardJobLocation__StyledTruncatedLocation-sc-1by41tq-1 kEinQH")
    #     # Create a dictionary to store the job information
    #     job_info = {
    #         "Job Title": job_title,
    #         "Company": company,
    #         "Location": location
    #     }

    #     # Add the job information to the job_data list
    #     job_data.append(job_info)

    #     # Check if the desired number of records has been reached
    #     if len(job_data) >= num_data:
    #         break

    # print(page_number)

    # # Check if there are no more pages to scrape
    # if not soup.find("a", class_="Pagination__NextLink-sc-16r01zq-2 fLLujR"):
    #     break
    
    # Increment the page number for the next iteration
    page_number += 1


df = pd.DataFrame(job_data)
script_dir = os.path.dirname(os.path.abspath(__file__))
custom_name = f'list_of_jobs_glints.csv'
file_path = os.path.join(script_dir, custom_name)
df.to_csv(file_path, index=False, encoding='utf-8')





    