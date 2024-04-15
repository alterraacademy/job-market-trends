import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Read data from CSV file
df = pd.read_csv('glints/list_of_jobs_glints_2.csv')

# Feature extraction
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['job_title'])

# Combine 'sub_category' and 'role' into a single column
y = df['sub_category'] + ' - ' + df['role']

# Train SVM classifier
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X, y)

def predict_job_title(job_title):
    # Vectorize input job title
    job_title_vectorized = vectorizer.transform([job_title])
    
    # Predict subcategory and role
    prediction = svm_classifier.predict(job_title_vectorized)
    predicted_sub_category, predicted_role = prediction[0].split(' - ')
    
    return predicted_sub_category, predicted_role

data_jobstreet = pd.read_csv('jobstreet/clean.csv')
job_title_jobstreet = data_jobstreet['Job Title']

predicted_job_titles = []
predicted_categories = []
predicted_roles = []

predicted_df = pd.DataFrame(columns=['job_title', 'predicted_subcategory', 'predicted_role'])
for job_title in job_title_jobstreet:
    predicted_subcategory, predicted_role= predict_job_title(job_title)
    predicted_job_titles.append(job_title)
    predicted_categories.append(predicted_subcategory)
    predicted_roles.append(predicted_role)

predicted_df = pd.DataFrame({
    'job_title': predicted_job_titles,
    'predicted_subcategory': predicted_categories,
    'predicted_role': predicted_roles
})

predicted_df.to_csv('jobstreet/predicted_jobstreet.csv', index=False)
