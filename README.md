# Job Market Trend Analysis 📊🏢💡

## Overview 👻
This project analyzes **job market trends** using Python. It scrapes job listings from websites, processes the data, and visualizes the trends over time. The analysis helps job seekers, recruiters, and researchers understand the current job market landscape. The project's output will be utilized by Alterra Academy to tailor their upcoming classes to meet industry demands.

## Features 📋
* **Web Scraping**: Utilizes BeautifulSoup and requests libraries to scrape job listings from various websites.
* **Data Processing**: Cleans and processes the scraped data to extract relevant information such as job title, company name, location, posted date, and requirements.
* **Data Visualization**: Uses matplotlib or other libraries to create visualizations like histograms, bar charts, and line graphs to showcase job trends.

## Getting Started 🚀
This Python script scrapes job listings from JobStreet Indonesia based on the specified position and location. It utilizes BeautifulSoup for web scraping and Selenium for navigating and extracting details from job detail pages.

### Prerequisites
Before you begin, make sure you have the following installed:
- Python 
- Jupyter Notebook/Google Collab
- Chrome WebDriver
- BeautifulSoup
- Requests
- Pandas
- Selenium

## Installation🛠️

### 🔗**Chrome WebDriver**
For using Selenium, first we need to download the Chrome WebDriver. To download it, follow these steps:
1. Check Chrome Version: Open Chrome and go to "Settings" > "About Chrome" to find your Chrome version.
2. Download WebDriver: Visit the Chrome WebDriver Downloads page.
3. Select Version: Download the WebDriver version that matches your Chrome version.
4. Extract File: Extract the downloaded file to get the WebDriver executable.
5. Set Path (Optional): Add the WebDriver executable to your system PATH or specify its location in your Selenium code.
6. Use WebDriver: Now you can use the WebDriver with Selenium for web automation.

### 🔗**Packages**
Install the required packages: BeautifulSoup, Requests, Pandas, Selenium

```bash
pip install requests beautifulsoup4 pandas selenium
```

### Usage 
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/alterraacademy/job-market-trends.git
2. Navigate to the project directory:
   ```bash
   cd job-market-trends
3. Open the `scraping_jobstreet.py` file in a Python environment
4. The script will scrape job listings and save them to CSV files based on the work type.

## Code Explanation 👀📖
### Jobstreet 
### 1. User Input 👩‍💻👨‍💻
The `search_position` and `location` variables are used to capture user input for the desired job position and location for job searching. The input is then processed to convert the text to lowercase and replace spaces with hyphens. This processing standardizes the input format for constructing the search URL.

```python
search_position = input('Enter Searched Position: ')
location = input('Enter Location: ')
search_position = search_position.lower().replace(' ','-')
location = location.lower().replace(' ','-')
```
- **`.lower()`**: Converts the input text to lowercase to ensure consistency.
- **`.replace(' ', '-')`**: Replaces spaces with hyphens to format the input for URLs (e.g., "data analyst" becomes "data-analyst").

### 2. Helper Function ⚡
The `find_tag_value` function is a helper function used to extract text content from HTML elements with a specific tag and attribute. It is primarily used in web scraping to extract data from web pages.

```python
def find_tag_value(soup, tag, attribute):
    try:
        return soup.find(tag, attrs={'data-automation':attribute}).text.strip()
    except AttributeError:
        return None
```
#### Parameters
- `soup`: A BeautifulSoup object representing the parsed HTML content of a web page.
- `tag`: The HTML tag name (e.g., 'a', 'span', 'div') of the element to find.
- `attribute`: The value of the 'data-automation' attribute used to identify the specific element.

#### Return Value
The function returns the text content of the found element after stripping any leading or trailing whitespace. If the element is not found or the attribute is not present, it returns `None`.
```python
job_title = find_tag_value(soup, 'a', 'jobTitle')
company_name = find_tag_value(soup, 'a', 'jobCompany')
```

### 3. Get the URL 🪝🌐
```python
page = 1
data = []
while True:
    base_url = 'https://www.jobstreet.co.id/id/'
    url_params = '{}-jobs/in-{}' if search_position and location else '{}-jobs' if search_position else 'jobs-in-{}' if location else 'jobs'

    url = base_url + url_params.format(search_position, location) + '?page={}'.format(page) if search_position or location else base_url + 'jobs?page={}'.format(page)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    job_cards = soup.find_all('article', attrs={'data-card-type': 'JobCard'})

        
    if len(job_cards) == 0:
        print('No More Jobs')
        break
    print('page',page,'jobs found', len(job_cards))

```
#### a. Initialization 
   - `page = 1`: Initializes a variable to track the page number of the job listings.
   - `data = []`: Initializes an empty list to store the extracted job data.

#### b. URL Construction
   - `base_url`: Sets the base URL for the JobStreet Indonesia website.
   - `url_params`: Defines a format string for constructing the URL based on search parameters (`search_position` and `location`).
   - `url`: Constructs the complete URL for the current page using `base_url`, `url_params`, `search_position`, `location`, and `page` number.

#### c. Fetching Job Listings
   - Sends a GET request to the constructed URL using `requests.get(url)`.
   - Parses the HTML content of the response using BeautifulSoup: `soup = BeautifulSoup(r.content, 'lxml')`.

#### d. Checking for Job Cards:
   - If no job cards are found on the page, it indicates that there are no more jobs to scrape. The loop breaks (`break`) out of the while loop.

#### e. Extracting Job Cards
   - Finds all job card elements (`<article>`) with the attribute `data-card-type` set to 'JobCard' using `soup.find_all('article', attrs={'data-card-type': 'JobCard'})`.
   - Each job card typically represents an individual job listing on the page.

This process repeats, incrementing `page` to scrape subsequent pages of job listings until no more job cards are found. The extracted job data is stored in the `data` list for further processing.

### 4. Job Card Data Extraction & Detail Page Navigation 🔎

#### a. Iterate Through Job Cards 
For each job card in job_cards, extract the **job title, company name, location, salary, job classification, job sub-classification, short job description, and posted date **using the `find_tag_value` function.
    
```python
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
```

- **`job_title`**: Extracts the job title using the find_tag_value function for the `<a>` tag with the attribute `jobTitle`.
- **`company_name`**: Extracts the company name using the find_tag_value function for the `<a>` tag with the attribute `jobCompany`.
- **`location_city`**: Extracts the job location (city) using the find_tag_value function for the `<a>` tag with the attribute `jobLocation`.
- **`salary`**: Extracts the job salary using the find_tag_value function for the `<span>` tag with the attribute `jobSalary`. It also removes any non-breaking space characters `(\xa0)`.
- **`job_classification`**: Extracts the job classification using the find_tag_value function for the `<a>` tag with the attribute `jobClassification`. It also removes any parentheses.
- **`job_sub_classification`**: Extracts the job sub-classification using the find_tag_value function for the `<a>` tag with the attribute `jobSubClassification`.
- **`job_short_desc`**: Extracts the short job description using the find_tag_value function for the `<span>` tag with the attribute `jobShortDescription`.
- **`posted_date`**: Extracts the job posting date using the find_tag_value function for the `<span>` tag with the attribute `jobListingDate`.

#### b. Extract Facility Information
Extracts the job facility information using the find_all method to find all `<li>` elements within the `<ul>` tag with specific classes. It then formats the facility list as a comma-separated string.
```python
facility = job_card.find('ul',class_='y735df0 y735df3 _1akoxc50 _1akoxc54')
if facility is not None:
    facility = facility.find_all('li')
    facility_list = [item.text.strip() for item in facility]
    facility_list = ', '.join(facility_list)
else:
    facility_list = ''
```

#### c. Extract More Detail Link
Extracts the URL for more job details using the find method to find the `<a>` tag with the attribute data-automation set to `job-list-view-job-link`. It then appends this URL to the base URL.
```python
more_detail_link = job_card.find('a', attrs={'data-automation':'job-list-view-job-link'})
if more_detail_link:
    more_detail_link = 'https://www.jobstreet.co.id'+ (more_detail_link.get('href'))
```

#### d. Navigate to Job Detail Page
- **Initialize WebDriver**: Creates a new instance of the Chrome WebDriver.
```python
driver = webdriver.Chrome()
```
- **Construct Job Details URL**: Uses the `job_id`, `search_position`, and `location` to construct the URL for the specific job's details page.
```python
job_detail_url = 'https://www.jobstreet.co.id/id/{}-jobs/in-{}?jobId={}&type=standout'.format(search_position, location, job_id)
```
- **Navigate to Job Details Page**: Uses `driver.get(job_detail_url)` to navigate to the constructed job details URL.
    
#### e. Find Job Details Section
- Wait for the job details section to be present on the page for a maximum 5 seconds.
```python
    wait = WebDriverWait(driver, 5)
    job_details_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobDetailsPage"]')))
```
- Uses `driver.page_source` to get the HTML content of the current page.
- Parses the HTML content using BeautifulSoup (`BeautifulSoup(driver.page_source, 'lxml')`) to create a BeautifulSoup object (`soup_job_detail_request`).
 ```python
 soup_job_detail_request = BeautifulSoup(driver.page_source, 'lxml')
 ```
- Finds the specific job details section (`<div>` with attribute `data-automation='jobDetailsPage'`) in the parsed HTML content.
```python
job_detail_page = soup_job_detail_request.find('div', attrs={'data-automation':'jobDetailsPage'})
```

#### f. Extract Work Type and Job Description
- Uses the `find_tag_value` function to extract the work type from the job details section.
- Uses the `find_tag_value` function to extract the job description from the job details section.
```python
     work_type = find_tag_value(job_detail_page, 'span', 'job-detail-work-type')
    job_desc = find_tag_value(job_detail_page, 'div', 'jobAdDetails')
```
    
#### g. Quit WebDriver
`driver.quit()`: Close the WebDriver to free up resources.   

#### h. Collect Extracted Data
The `data.append()` method is used to collect the extracted details of each job listing into **a list of dictionaries**. Each dictionary represents one job listing with its corresponding details.

```python
data.append({
    'Job Title': job_title,
    'Company Name': company_name,
    'Location': location_city,
    'Salary': salary,
    'Work Type': work_type,
    'Job Classification': job_classification,
    'Job Sub Classification': job_sub_classification,
    'Job Short Description': job_short_desc,
    'Job Description': job_desc,
    'Facility': facility_list,
    'Posted Date': posted_date
})
```
#### i. Increment Page Number
Increment the `page` variable to move to the next page of job listings.

### 5. Creating a DataFrame from Extracted Job Data 
- The `pd.DataFrame(data)` function converts the extracted job data (stored in the `data` list) into a tabular format called a DataFrame.
- Each dictionary in the `data` list becomes a row in the DataFrame, with keys becoming column names.

  
# TimesJob
### Scraping from TimesJob Website
1. Open the `job_scraping.py` file and customize the `position` and `location` variables in the __main__ block according to your requirements.
   ```bash
   python job_scraping.py

2. The script will print the number of jobs found and the URL for each page it scrapes. 
3. Install the required packages:
    ```bash
    pip install requests beautifulsoup4 datetime pandas matplotlib urllib

## Scraping Job Listings 
When you're web scraping, you're creating a program to fetch the underlying code of a webpage, which is written in HTML. 


- position: Specify the job position you want to search for (e.g., 'data analyst').
- location: Specify the location for the job search. Leave it empty for a broader search.

### URL Encoding
Before making the request, the position and location parameters are URL-encoded using urllib.parse.quote_plus. This ensures that special characters in the position and location strings are properly encoded for the URL.

```python
position = urllib.parse.quote_plus(position)
location = urllib.parse.quote_plus(location)
```
### Pagination
- The scraping is done in a loop to handle pagination. The sequence variable is used to track the current page number. The URL template includes the sequence and startPage parameters, which are used to navigate through the paginated results.
- Inside the loop, after fetching and parsing the HTML content, the script checks if there are any job listings by using the condition `if not jobs:`. If `jobs` is an empty list (meaning no job listings were found on the current page), it indicates that there are no more jobs to scrape.
- When no jobs are found, the script executes `break`, which exits the loop and ends the scraping process.

```python
while True:
start_page = 1 + ((sequence - 1) // 10) * 10

if not jobs:
      break
  sequence += 1
```
### Fetch URL
  The HTML content of the page is fetched using requests.get(url).text and parsed using BeautifulSoup.
  1. URL Template & Constructing the URL
  - The template variable stores a URL template for the TimesJobs search page. It contains placeholders ({}) for the position, location, sequence, and start page number. These placeholders will be replaced with actual values when the URL is constructed.
    ```python
    template = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=100&txtKeywords=0DQT0{}0DQT0&postWeek=60&searchType=personalizedSearch&actualTxtKeywords {}&searchBy=0&rdoOperator=OR&txtLocation={}&pDate=I&sequence={}&startPage={}'
    url = template.format(position,position, location, sequence, start_page)
    ```
  2. Making the HTTP Request
  - The requests.get(url) function sends an HTTP GET request to the URL constructed in the previous step and retrieves the HTML content of the page.
  ```python
    html_text = requests.get(url).text
  ```
  3. Parsing the HTML
  - The `BeautifulSoup` class is used to parse the HTML content retrieved from the website. The 'lxml' argument specifies the parser to be used by BeautifulSoup.
    ```python
        soup = BeautifulSoup(html_text, 'lxml')
    ```
### Finding Job Listings
  Searches the parsed HTML for all `<li>` elements with the specified class, which typically represent job listings.
    ```python
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  
    print('jobs found', len(jobs), 'url', url)  
    ```
### Extracting Job Details
For each job listing, the code extracts the following details:

  - Job role (job_role)
  - Company name (company_name)
  - Location of the job (location_company)
  - Date the job was posted (posted_date)
  - Required skills (skill)
  - Job description (job_desc)
  - Link to more details (more_detail_link)
    
    ```python
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
                years_exp = job.select_one('ul.top-jd-dtl li:has(i.material-icons:contains("card_travel"))').text.replace('card_travel', '').strip()
            except AttributeError:
                experience = ''
            try:
                more_detail_link = job.header.h2.a['href']
            except AttributeError:
                more_detail_link = ''
            
            extract_date = datetime.today().strftime('%Y-%m-%d')
    ```

### Execution Block
```python
if __name__ == '__main__':
    position = 'data analyst'
    location = ''
    scrape_jobs(position, location)
```
* **Storing the Data**
The extracted job details are stored in a list of dictionaries `(data)`. Each dictionary represents a single job listing. After scraping all the job listings, the data is converted into a pandas `DataFrame` `(df)`.
  ```python
  data.append({'Role':job_role, 'Company Name':company_name, 'Location':location_company, 'Posted Date':posted_date,'Extracted Date':extract_date,'Key Skill': skill,'Job Description':job_desc, 'More Detail':more_detail_link})
  ```
* **Saving to CSV**
Finally, the DataFrame is saved to a CSV file using the `to_csv` method. The file is named `list_of_{position}_timesjobs.csv`, where {position} is the URL-encoded version of the original position parameter.
  ```python
    df = pd.DataFrame(data)
    df.to_csv(f'list_of_{position}_timesjobs.csv', index=False, encoding='utf-8')
```
