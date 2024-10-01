from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load the fine-tuned model
fine_tuned_model = SentenceTransformer('./fine-tuned-model')

# Function to encode text
courses_df = pd.read_excel('C:/Users/13054/Desktop/Re-created jobspy project/course_descriptions.xlsx')

# Load cleaned job descriptions
jobs_df = pd.read_excel('C:/Users/13054/Desktop/Re-created jobspy project/cleaned_jobs.xlsx')
def encode_text(text, model):
    return model.encode(text)

# Calculate embeddings for course and job descriptions using the fine-tuned model
courses_df['fine_tuned_embedding'] = courses_df['filtered_description'].apply(lambda x: encode_text(x, fine_tuned_model))
jobs_df['fine_tuned_embedding'] = jobs_df['cleaned_description'].apply(lambda x: encode_text(x, fine_tuned_model))

# Initialize a list to hold the results
fine_tuned_matching_results = []

# Compare each course with each job using the fine-tuned model
for _, course in courses_df.iterrows():
    course_embedding = course['fine_tuned_embedding']
    for _, job in jobs_df.iterrows():
        job_embedding = job['fine_tuned_embedding']
        similarity = util.pytorch_cos_sim(course_embedding, job_embedding).item()
        fine_tuned_matching_results.append({
            'Course Name': course['course_name'],
            'Job Title': job['title'],
            'Similarity': similarity,
            'Salary': job['mean_salary'],
            'Is Core': course['is_core']
        })

# Convert results to DataFrame
fine_tuned_matches_df = pd.DataFrame(fine_tuned_matching_results)
print(fine_tuned_matches_df)

# Export the results to a CSV file
fine_tuned_matches_path = 'C:/Users/13054/Desktop/Re-created jobspy project/Datasets/fine_tuned_matching.csv'
fine_tuned_matches_df.to_csv(fine_tuned_matches_path, index=False)

print("Fine-tuned matching results saved to", fine_tuned_matches_path)