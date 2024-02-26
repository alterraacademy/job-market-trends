FROM python:3.10.6
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x job_scraping.py
CMD [ "python", "./job_scraping.py" ] 