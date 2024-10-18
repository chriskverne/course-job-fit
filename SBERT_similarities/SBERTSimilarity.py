import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

def get_mean_pooled_embedding(text, model, tokenizer):
    tokens = tokenizer(text, truncation=False, return_tensors='pt')['input_ids'][0]
    # Split tokens into chunks of max 512 tokens
    chunks = [tokens[i:i + 512] for i in range(0, len(tokens), 512)]

    # Compute embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        inputs = tokenizer.decode(chunk, skip_special_tokens=True)
        embeddings.append(model.encode(inputs, convert_to_tensor=True))

    # Mean pooling across all chunks
    mean_embedding = torch.mean(torch.stack(embeddings), dim=0)
    return mean_embedding


def calculate_similarity(course_path, output_path, job_path):
    # Load cleaned course and job descriptions
    courses_df = pd.read_excel(course_path)
    jobs_df = pd.read_excel(job_path)

    # Initialize the SBERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    tokenizer = model.tokenizer

    # Extract the course descriptions and job descriptions
    course_names = courses_df['Course Name'].tolist()
    course_descriptions = courses_df['Course Description'].tolist()

    job_titles = jobs_df['title'].tolist()
    job_descriptions = jobs_df['cleaned_description'].tolist()
    job_salaries = jobs_df['mean_salary'].tolist()

    # Counter for truncations
    truncation_count = 0
    tt_count = 0

    # Compute embeddings for course descriptions
    course_embeddings = []
    for description in course_descriptions:
        tokens = tokenizer(description, truncation=False)['input_ids']
        if len(tokens) > 512:
            truncation_count += 1
            embedding = get_mean_pooled_embedding(description, model, tokenizer)
        else:
            embedding = model.encode(description, convert_to_tensor=True)
        course_embeddings.append(embedding)
        tt_count += 1

    # Compute embeddings for job descriptions
    job_embeddings = []
    for description in job_descriptions:
        tokens = tokenizer(description, truncation=False)['input_ids']
        if len(tokens) > 512:
            truncation_count += 1
            embedding = get_mean_pooled_embedding(description, model, tokenizer)
        else:
            embedding = model.encode(description, convert_to_tensor=True)
        job_embeddings.append(embedding)
        tt_count += 1

    print(f"Total descriptions truncated: {truncation_count}, tt_description : {tt_count}")

    # Convert lists to tensors for similarity calculation
    course_embeddings = torch.stack(course_embeddings)
    job_embeddings = torch.stack(job_embeddings)

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
    results_df.to_csv(output_path, index=False)

    print(f"Similarity between courses and jobs calculated and saved to '{output_path}'.")


# Paths for datasets and outputs
core_path = '../../Datasets/cleaned_core_courses.xlsx'
core_output = './core_course_job_similarity.csv'

elective_path = '../../Datasets/cleaned_elective_courses.xlsx'
elective_output = './elective_course_job_similarity.csv'

all_path = '../Datasets/cleaned_all_courses.xlsx'
all_output = './all_course_job_similarity.csv'

# Calculate similarity for the all courses dataset
calculate_similarity(all_path, all_output, '../Datasets/final_jobs.xlsx')
