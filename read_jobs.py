import pandas as pd
import re
from nltk.corpus import stopwords
import nltk

# Load stopwords
stop_words = set(stopwords.words('english'))

# Function to clean the job description text
def clean_description(description):
    if pd.isnull(description):
        return ""
    # Convert to lowercase
    description = description.lower()

    # Remove non-alphabetical characters
    description = re.sub('[^a-zA-Z]', ' ', description)

    # Remove extra whitespace
    description = re.sub(r'\s+', ' ', description)

    # Tokenize and remove stopwords
    words = description.split()
    filtered_description = ' '.join([word for word in words if word not in stop_words])

    return filtered_description

def clean_data(df, output_path):
    # Convert salaries to numeric values
    df['min_amount'] = pd.to_numeric(df['min_amount'], errors='coerce')
    df['max_amount'] = pd.to_numeric(df['max_amount'], errors='coerce')

    # Convert hourly to yearly salaries (Multiply by 40 (hours per week) and 52 (weeks a year))
    df.loc[df['interval'] == 'hourly', 'min_amount'] = df['min_amount'] * 40 * 52
    df.loc[df['interval'] == 'hourly', 'max_amount'] = df['max_amount'] * 40 * 52

    # Get average salary (by looking at salary range)
    df['mean_salary'] = (df['min_amount'] + df['max_amount']) / 2

    # Print number of jobs that have no description
    missing_descriptions_count = df['description'].isnull().sum()
    print(f"Number of jobs without a description: {missing_descriptions_count}")

    # Drop rows where the job description is NaN
    df = df.dropna(subset=['description'])

    # Apply text cleaning function to job descriptions
    df['cleaned_description'] = df['description'].apply(clean_description)

    # Save the cleaned data to a new Excel file
    df.to_excel(output_path, index=False)

# Clean the dataset
df = pd.read_excel('./Datasets/swe_jobs_10_08.xlsx')
output_path = './Datasets/cleaned_tech_jobs3.xlsx'
clean_data(df, output_path)