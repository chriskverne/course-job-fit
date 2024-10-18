import pandas as pd

# Load the datasets
df_cs = pd.read_excel('./cleanedJobs/cleaned_all_cs_jobs.xlsx')
df_ds = pd.read_excel('./cleanedJobs/cleaned_all_ds_jobs.xlsx')
df_it = pd.read_excel('./cleanedJobs/cleaned_all_it_jobs.xlsx')
df_pm = pd.read_excel('./cleanedJobs/cleaned_all_pm_jobs.xlsx')
df_swe = pd.read_excel('./cleanedJobs/cleaned_all_swe_jobs.xlsx')

# Sample the required number of jobs from each category
df_swe_sample = df_swe.sample(n=7000, random_state=42)  # 7000 random SWE jobs
df_pm_sample = df_pm.sample(n=1000, random_state=42)    # 1000 random PM jobs
df_it_sample = df_it.sample(n=1000, random_state=42)    # 1000 random IT jobs
df_ds_sample = df_ds.sample(n=500, random_state=42)     # 500 random Data Science jobs
df_cs_sample = df_cs.sample(n=500, random_state=42)     # 500 random Cybersecurity jobs

# Combine all samples into one final dataset
df_final = pd.concat([df_swe_sample, df_pm_sample, df_it_sample, df_ds_sample, df_cs_sample])

# Save the final combined dataset
df_final.to_excel('../Datasets/final_jobs.xlsx', index=False)

print(f"Final dataset has {df_final.shape[0]} jobs.")
