import pandas as pd

df = pd.read_excel('C:/Users/13054/Desktop/Re-created jobspy project/cleaned_jobs.xlsx')

print(len(df[df['mean_salary'] > 100000]))