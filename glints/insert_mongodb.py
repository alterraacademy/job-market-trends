from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)  # Assuming MongoDB is running on localhost:27017
db = client['jobs']  # Connect to the database

# Access collections
job_collection = db['glints_data']  # Access the glints_data collection
location_collection = db['locations']  # Access the locations collection

# Iterate over each document in the glints_data collection
for job_document in job_collection.find():
    # Find the corresponding location in the locations collection
    location = location_collection.find_one({
        'district': job_document['district'],
        'city': job_document['city'],
        'province': job_document['province']
    })
    
    # If a matching location is found, add its ID to the job document
    if location:
        job_collection.update_one({'_id': job_document['_id']}, {'$set': {'location_id': location['_id']}})
    else:
        # Handle missing location data
        job_collection.update_one({'_id': job_document['_id']}, {'$set': {'location_id': None}})

# Close MongoDB connection
#client.close()
