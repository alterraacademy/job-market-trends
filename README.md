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
- Jupyter Notebook (optional, but recommended for interactive development)

## Usage
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/alterraacademy/job-scraper.git
2. Navigate to the project directory:
   ```bash
   cd job-scraper
3. Open the `job_scraping.py` file and customize the `position` and `location` variables in the __main__ block according to your requirements.
   ```bash
   python job_scraping.py
4. The script will print the number of jobs found and the URL for each page it scrapes. 
5. Install the required packages:
    ```bash
    pip install requests beautifulsoup4 datetime pandas matplotlib urllib

## Scraping Job Listings 
When you're web scraping, you're creating a program to fetch the underlying code of a webpage, which is written in HTML. In this context, we're scraping job listings from **TimesJobs**, we'd use a function called **scrape_jobs** to **extract jobs based on the position and location specified.**
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
