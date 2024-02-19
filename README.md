# Job Market Trend Analysis 📊🏢💡

## Overview
This project analyzes **job market trends** using Python. It scrapes job listings from websites, processes the data, and visualizes the trends over time. The analysis helps job seekers, recruiters, and researchers understand the current job market landscape. The project's output will be utilized by Alterra Academy to tailor their upcoming classes to meet industry demands.
## Features
* **Web Scraping**: Utilizes BeautifulSoup and requests libraries to scrape job listings from various websites.
* **Data Processing**: Cleans and processes the scraped data to extract relevant information such as job title, company name, location, posted date, and requirements.
* **Data Visualization**: Uses matplotlib or other libraries to create visualizations like histograms, bar charts, and line graphs to showcase job trends.

## Getting Started
### Prerequisites
Before you begin, make sure you have the following installed:
- Python 3
- Jupyter Notebook (optional, but recomjob-trend-analysis\Scripts\activate
mended for interactive development)

## Setting up your Environment
  1. Create a new Python virtual environment:
     ```bash
     python3 -m venv job-trend-analysis
  2. Activate the virtual environment:
     - On Windows:
       ```bash
       job-trend-analysis\Scripts\activate

     - On macOS and Linux:
       ```bash
       source job-trend-analysis/bin/activate

3.  Install the required packages:
    ```bash
    pip install requests beautifulsoup4 datetime pandas matplotlib urllib
## Scraping Job Listings
The scrape_jobs function is used to scrape job listings from the TimesJobs website based on the specified position and location.

* **URL Encoding**
Before making the request, the position and location parameters are URL-encoded using urllib.parse.quote_plus. This ensures that special characters in the position and location strings are properly encoded for the URL.
  ```bash
  position = urllib.parse.quote_plus(position)
  location = urllib.parse.quote_plus(location)
  
* **Pagination**
The scraping is done in a loop to handle pagination. The sequence variable is used to track the current page number. The URL template includes the sequence and startPage parameters, which are used to navigate through the paginated results.
  ```bash
  start_page = 1 + ((sequence - 1) // 10) * 10

* **Fetch URL**
  The HTML content of the page is fetched using requests.get(url).text and parsed using BeautifulSoup.
  The job listings are typically contained within <li> elements with the class clearfix job-bx wht-shd-bx.
  ```bash
  template = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=100&txtKeywords=0DQT0{}0DQT0&postWeek=60&searchType=personalizedSearch&actualTxtKeywords {}&searchBy=0&rdoOperator=OR&txtLocation={}&pDate=I&sequence={}&startPage={}'
  url = template.format(position,position, location, sequence, start_page)
  html_text = requests.get(url).text
  
* **Extracting Job Details**
For each job listing, the code extracts the following details:

  - Job role (job_role)
  - Company name (company_name)
  - Location of the job (location_company)
  - Date the job was posted (posted_date)
  - Required skills (skill)
  - Job description (job_desc)
  - Link to more details (more_detail_link)
    ```bash
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
                location_company = job.find('span').text.strip()
            except AttributeError:
                location_company = ''
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
            
            extract_date = datetime.today().strftime('%Y-%m-%d')
            
    
* **Storing the Data**
The extracted job details are stored in a list of dictionaries (data). Each dictionary represents a single job listing. After scraping all the job listings, the data is converted into a pandas DataFrame (df).
  ```bash
  data.append({'Role':job_role, 'Company Name':company_name, 'Location':location_company, 'Posted Date':posted_date,'Extracted Date':extract_date,'Key Skill': skill,'Job Description':job_desc, 'More Detail':more_detail_link})
  
* **Saving to CSV**
Finally, the DataFrame is saved to a CSV file using the to_csv method. The file is named list_of_{position}_timesjobs.csv, where {position} is the URL-encoded version of the original position parameter.
  ```bash
    df = pd.DataFrame(data)
    df.to_csv(f'list_of_{position}_timesjobs.csv', index=False, encoding='utf-8')
