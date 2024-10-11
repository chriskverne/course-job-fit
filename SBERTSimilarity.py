import pandas as pd
from sentence_transformers import SentenceTransformer, util

def calculate_similarity(course_path, output_path, job_path):
    # Load cleaned course and job descriptions
    courses_df = pd.read_excel(course_path)
    jobs_df = pd.read_excel(job_path)

    # Initialize the SBERT model
    model = SentenceTransformer('all-MiniLM-L6-v2') 

    # Extract the course descriptions and job descriptions
    course_names = courses_df['Course Name'].tolist()
    course_descriptions = courses_df['Course Description'].tolist()

    job_titles = jobs_df['title'].tolist()
    job_descriptions = jobs_df['cleaned_description'].tolist()
    job_salaries = jobs_df['mean_salary'].tolist()

    # Compute embeddings for course descriptions and job descriptions
    course_embeddings = model.encode(course_descriptions, convert_to_tensor=True)
    job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

    # Compute cosine similarities between each course and job description
    similarity_matrix = util.cos_sim(course_embeddings, job_embeddings)

    # Create a list to store the results in the desired format
    results = []

    # Loop through each course and job to create a flat structure
    for i, course_name in enumerate(course_names):
        for j, job_title in enumerate(job_titles):
            similarity_score = similarity_matrix[i][j].item()  # Get similarity score
            job_salary = job_salaries[j]  # Get the salary for the job
            results.append([course_name, job_title, similarity_score, job_salary])

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=['Course Name', 'Job Title', 'Similarity', 'Job Salary'])

    # Save the similarity results to an Excel file
    results_df.to_excel(output_path, index=False)

    print(f"Similarity between courses and jobs calculated and saved to '{output_path}'.")

core_path = './Datasets/cleaned_core_courses.xlsx'
core_output = './SBERT_similarities/core_course_job_similarity.xlsx'

elective_path = './Datasets/cleaned_elective_courses.xlsx'
elective_output = './SBERT_similarities/elective_course_job_similarity.xlsx'

all_path = './Datasets/cleaned_all_courses.xlsx'
all_output = './SBERT_similarities/all_course_job_similarity.xlsx'

#calculate_similarity(core_path, core_output, './Datasets/cleaned_tech_jobs3.xlsx')
#calculate_similarity(elective_path, elective_output, './Datasets/cleaned_tech_jobs3.xlsx')
calculate_similarity(all_path, all_output, './Datasets/cleaned_tech_jobs3.xlsx')
