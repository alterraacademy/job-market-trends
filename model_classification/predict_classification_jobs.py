import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

df = pd.read_csv('glints/list_of_jobs_glints_2.csv')

# Feature extraction
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['job_title'])

# dense_matrix = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
# frontend_scores = dense_matrix['frontend']
# backend_scores = dense_matrix['backend']
# avg_frontend_score = frontend_scores.mean()
# avg_backend_score = backend_scores.mean()
# top_frontend_titles = df.loc[frontend_scores.nlargest(5).index]['job_title']
# top_backend_titles = df.loc[backend_scores.nlargest(5).index]['job_title']

# print(dense_matrix)
# print(frontend_scores)
# print(backend_scores)
# print(avg_frontend_score)
# print(avg_backend_score)
# print(top_frontend_titles)
# print(top_backend_titles)

y = df['sub_category'] + ' - ' + df['role']

# Train SVM classifier
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X, y)

def predict_job_title(job_title):
    # split input into each word
    words = job_title.split()
    
    # Vectorize input job title
    job_title_vectorized = vectorizer.transform([job_title])
    
    # Predict subcategory and role
    prediction = svm_classifier.predict(job_title_vectorized)
    predicted_sub_category, predicted_role = prediction[0].split(' - ')
    
    return predicted_sub_category, predicted_role

# sub_cat, role = predict_job_title('Front End Developer')
# print(sub_cat, role)


data_jobstreet = pd.read_csv('glints/role.csv')
job_title_jobstreet = data_jobstreet['job_title']

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

predicted_df.to_csv('glints/predicted_glints.csv', index=False)
