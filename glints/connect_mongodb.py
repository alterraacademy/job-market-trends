import pymongo
from pymongo import MongoClient
import pandas as pd 

df = pd.read_csv('glints/list_of_jobs_glints_2.csv')

data_dict = df.to_dict("records")

client = MongoClient('mongodb://localhost:27017/')
db = client['jobs']
collection = db['glints_data']

collection.insert_many(data_dict)

location_collection = db['locations']
location_data = df[['district', 'city', 'province']].drop_duplicates().to_dict(orient='records')
location_ids = location_collection.insert_many(location_data).inserted_ids

job_collection = db['glints_data']

for index, row in df.iterrows():
    location = location_collection.find_one({'district': row['district'], 'city': row['city'], 'province': row['province']})
    if location:
        row['location_id'] = location['_id']
    else:
        row['location_id'] = None  # Handle missing location data
    
    job_collection.insert_one(row.to_dict())
