import pandas as pd
from fontTools.subset import subset

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

combine_dataframes(pm_paths)