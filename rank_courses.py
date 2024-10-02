import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('./Datasets/core_course_job_similarity.xlsx')
df.reset_index()

high_sim = df[df['Similarity'] > 0.60]  # df.groupby('Course Name')['Similarity'] > 0.7
high_sim_count = high_sim.groupby('Course Name').size().sort_values()

print(high_sim_count)