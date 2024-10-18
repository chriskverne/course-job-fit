import pandas as pd
import re
from Functions.CleanText import clean_text

swe_paths = [
    './jobs/swe_jobs_10_05.xlsx',
    './jobs/swe_jobs_10_08.xlsx',
    './jobs/swe_jobs_10_10.xlsx',
    './jobs/swe_jobs_10_13.xlsx',
    './jobs/swe_jobs_10_16.xlsx',
    './jobs/swe_jobs_10_17.xlsx'
]
cs_paths = [
    './jobs/cs_jobs_10_10.xlsx',
    './jobs/cs_jobs_10_13.xlsx',
    './jobs/cs_jobs_10_16.xlsx',
    './jobs/cs_jobs_10_17.xlsx'
]
ds_paths = [
    './jobs/ds_jobs_10_10.xlsx',
    './jobs/ds_jobs_10_13.xlsx',
    './jobs/ds_jobs_10_16.xlsx',
    './jobs/ds_jobs_10_17.xlsx',
]
it_paths = [
    './jobs/it_jobs_10_13.xlsx',
    './jobs/it_jobs_10_16.xlsx',
    './jobs/it_jobs_10_17.xlsx',
]
pm_paths = [
    './jobs/pm_jobs_10_10.xlsx',
    './jobs/pm_jobs_10_13.xlsx',
    './jobs/pm_jobs_10_17.xlsx',
]

def combine_dataframes(paths):
    tt_jobs = 0
    valid_jobs = 0
    all_dfs = []

    for path in paths:
        df = pd.read_excel(path)
        tt_jobs += df.shape[0]
        # Remove Empty Job Descriptions
        df.dropna(subset=['description'], inplace=True)
        valid_jobs += df.shape[0]
        # Add dataframe to combined dataframe
        all_dfs.append(df)

    # Combine all dataframes to 1 large one
    combined_df = pd.concat(all_dfs)
    # Drop duplicate job postings
    combined_df.drop_duplicates(subset=['description'], inplace=True)

    # Results
    print(f'TT_JOBS: {tt_jobs} NON_EMPTY_JOBS: {valid_jobs} UNIQUE_VALID_JOBS: {combined_df.shape[0]}')

    return combined_df

# Load stopwords
def clean_data(df, output_path):
    df = df.reset_index(drop=True)

    # Convert salaries to numeric values
    df['min_amount'] = pd.to_numeric(df['min_amount'], errors='coerce')
    df['max_amount'] = pd.to_numeric(df['max_amount'], errors='coerce')

    # Convert hourly to yearly salaries (Multiply by 40 (hours per week) and 52 (weeks a year))
    df.loc[df['interval'] == 'hourly', 'min_amount'] = df['min_amount'] * 40 * 52
    df.loc[df['interval'] == 'hourly', 'max_amount'] = df['max_amount'] * 40 * 52

    # Get average salary (by looking at salary range)
    df['mean_salary'] = (df['min_amount'] + df['max_amount']) / 2

    # Drop rows where the job description is NaN
    df = df.dropna(subset=['description'])

    # Apply text cleaning function to job descriptions
    df['cleaned_description'] = df['description'].apply(clean_text)

    # Save the cleaned data to a new Excel file
    df.to_excel(output_path, index=False)

# Clean the dataset
combined_df = combine_dataframes(pm_paths)
output_path =  './cleanedjobs/cleaned_all_pm_jobs.xlsx'
clean_data(combined_df, output_path)