from jobspy import scrape_jobs
import pandas as pd
from IPython.display import display, HTML
# ['indeed', 'zip_recruiter', 'linkedin']

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

#search_term = "software engineer",
#search_term = "data scientist",
#search_term = "product manager",
#search_term = "cyber security",
#search_term = "IT",

# Others: consultant, technical analyst, quant finance, manaegement (This study addresses more broad roles that most CS students usually will get in to)
# Don't do 'linkedin' as it can tend to block requests

def scrape_jobs_from_site(path, res_wanted, job):
    jobs = scrape_jobs(
        site_name= ['zip_recruiter', 'glassdoor', 'indeed'],
        location='USA',
        search_term=job,
        results_wanted=res_wanted,
        hours_old=24, # 24hr
        linkedin_fetch_description=True,
        country_indeed='USA'
    ) 

    jobs.to_excel(path)

# Swe Jobs
swe_path = './jobs/swe_jobs_10_10.xlsx'
swe_res = 2000
swe_term = "Software engineer"
#scrape_jobs(swe_path, swe_res, swe_term)

# Data science Jobs
ds_path = './jobs/ds_jobs_10_10.xlsx'
ds_res = 500
ds_term = "Data scientist"
#scrape_jobs_from_site(ds_path, ds_res, ds_term)

# Cyber security Jobs
cs_path = './jobs/cs_jobs_10_10.xlsx'
cs_res = 500
cs_term = "Cyber Security"
#scrape_jobs_from_site(cs_path, cs_res, cs_term)

# Product managment Jobs
pm_path = './jobs/pm_jobs_10_10.xlsx'
pm_res = 500
pm_term = "Technical product manager"
#scrape_jobs_from_site(pm_path, pm_res, pm_term)