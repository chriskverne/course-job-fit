import pandas as pd

df = pd.read_excel('./Datasets/elective_course_job_similarity.xlsx')
df.reset_index()

avg_sims = df.groupby('Course Name')['Similarity'].mean().sort_values()
print(avg_sims)

high_sims_jobs = df[df['Similarity'] > 0.50].groupby('Course Name').size().sort_values()
print(high_sims_jobs)


#plt.figure()
#high_sim_count.plot(kind='barh')
#plt.show()