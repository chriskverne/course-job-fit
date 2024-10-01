import pandas as pd
import spacy

jobs_df = pd.read_excel('C:/Users/13054/Desktop/Re-created jobspy project/jobs2.xlsx')

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

# Function to clean text using SpaCy
def clean_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

# Delete Jobs without minimum and maximum salary Posted
jobs_df.dropna(subset=['min_amount', 'max_amount'], how='all', inplace=True)

# Update jobs with hourly salary to yearly salary
hourly_threshold = 1000

# Identify potential hourly salaries in both min_amount and max_amount columns
potential_hourly_min_mask = jobs_df['min_amount'] < hourly_threshold
potential_hourly_max_mask = jobs_df['max_amount'] < hourly_threshold

# Convert potential hourly salaries to annual (40 hours/week * 52 weeks/year)
jobs_df.loc[potential_hourly_min_mask, 'min_amount'] *= 40 * 52
jobs_df.loc[potential_hourly_max_mask, 'max_amount'] *= 40 * 52

# Create Mean Salary
jobs_df['mean_salary'] = (jobs_df['min_amount'] + jobs_df['max_amount']) / 2

# Clean job descriptions using SpaCy
jobs_df['cleaned_description'] = jobs_df['description'].apply(clean_text)

# Save the cleaned job descriptions to a new Excel file
cleaned_jobs_path = 'C:/Users/13054/Desktop/Re-created jobspy project/cleaned_jobs.xlsx'
jobs_df.to_excel(cleaned_jobs_path, index=False)

print("Cleaned job descriptions saved to", cleaned_jobs_path)
