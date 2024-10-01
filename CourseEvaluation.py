import pandas as pd

def rank_courses(df, wanted_salary=None):
    # Define thresholds for strong match and high salary
    strong_match_threshold = df['Similarity'].quantile(0.75)  # 75th percentile for strong match
    if wanted_salary is None:
        high_salary_threshold = df['Salary'].quantile(0.5)  # 50th percentile for high salary
    else:
        high_salary_threshold = wanted_salary

    # Filter for strong matches
    strong_matches = df[df['Similarity'] >= strong_match_threshold]

    # Count strong matches per course
    strong_match_counts = strong_matches['Course Name'].value_counts().reset_index()
    strong_match_counts.columns = ['Course Name', 'Strong Match Count']

    # Filter for strong matches and high salaries
    strong_high_matches = df[(df['Similarity'] >= strong_match_threshold) & (df['Salary'] > high_salary_threshold)]

    # Count strong high-salary matches per course
    strong_high_match_counts = strong_high_matches['Course Name'].value_counts().reset_index()
    strong_high_match_counts.columns = ['Course Name', 'Strong-High Match Count']

    # Calculate average similarity for all matches
    avg_all_similarity = df.groupby('Course Name')['Similarity'].mean().reset_index()
    avg_all_similarity.columns = ['Course Name', 'Average Similarity']

    # Calculate the average sum of similarities across all courses
    avg_sum_of_similarities = df.groupby('Course Name')['Similarity'].sum().max()

    # Calculate weighted mean salary for each course
    def calculate_weighted_mean_salary(group):
        weighted_salary = (group['Salary'] * group['Similarity']).sum()
        total_similarity = group['Similarity'].sum()
        return weighted_salary / avg_sum_of_similarities

    weighted_mean_salary = df.groupby('Course Name').apply(calculate_weighted_mean_salary).reset_index()
    weighted_mean_salary.columns = ['Course Name', 'Weighted Mean Salary']

    # Merge the counts, similarities, and weighted mean salary
    course_rankings = pd.merge(strong_match_counts, strong_high_match_counts, on='Course Name', how='outer')
    course_rankings = pd.merge(course_rankings, avg_all_similarity, on='Course Name', how='outer')
    course_rankings = pd.merge(course_rankings, weighted_mean_salary, on='Course Name', how='outer')

    # Fill NaN values with 0 for counts and weighted mean salary
    course_rankings['Strong Match Count'] = course_rankings['Strong Match Count'].fillna(0).astype(int)
    course_rankings['Strong-High Match Count'] = course_rankings['Strong-High Match Count'].fillna(0).astype(int)
    course_rankings['Weighted Mean Salary'] = course_rankings['Weighted Mean Salary'].fillna(0)

    # Include courses with 0 strong matches
    all_courses = df['Course Name'].unique()
    zero_match_courses = set(all_courses) - set(course_rankings['Course Name'])
    zero_match_df = pd.DataFrame(zero_match_courses, columns=['Course Name'])
    zero_match_df['Strong Match Count'] = 0
    zero_match_df['Strong-High Match Count'] = 0
    zero_match_df['Average Similarity'] = df[df['Course Name'].isin(zero_match_courses)].groupby('Course Name')['Similarity'].mean().values
    zero_match_df['Weighted Mean Salary'] = 0  # Courses with zero matches have a weighted mean salary of 0

    # Combine with main rankings
    course_rankings = pd.concat([course_rankings, zero_match_df], ignore_index=True)

    # Calculate ranks for each metric
    course_rankings['Rank Average Similarity'] = course_rankings['Average Similarity'].rank(ascending=False)
    course_rankings['Rank Strong-High Match Count'] = course_rankings['Strong-High Match Count'].rank(ascending=False)
    course_rankings['Rank Strong Match Count'] = course_rankings['Strong Match Count'].rank(ascending=False)
    course_rankings['Rank Weighted Mean Salary'] = course_rankings['Weighted Mean Salary'].rank(ascending=False)

    # Calculate combined rank
    course_rankings['Combined Rank'] = (
        (course_rankings['Rank Average Similarity'] +
        course_rankings['Rank Strong-High Match Count'] +
        course_rankings['Rank Strong Match Count'] +
        course_rankings['Rank Weighted Mean Salary'])/4
    )

    # Sort by Combined Rank
    course_rankings = course_rankings.sort_values(by='Combined Rank')

    return course_rankings

# Load the data
df = pd.read_csv('C:/Users/13054/Desktop/Re-created jobspy project/Datasets/fine_tuned_matching.csv')

# Total Rankings
all_course_rankings = rank_courses(df, wanted_salary=100000)

# Add 'Is Core' columns
all_course_rankings = pd.merge(all_course_rankings, df[['Course Name', 'Is Core']].drop_duplicates(), on='Course Name', how='left')

# Save the results to a CSV file
all_course_rankings.to_csv('C:/Users/13054/Desktop/Re-created jobspy project/Datasets/all_fine_tuned_course_rankings.csv', index=False)

# Print the results
print("Classes ranked by strong matches to high-paying jobs and average similarity:")
print(all_course_rankings.to_markdown(index=False))

print(f"Saved results to 'C:/Users/13054/Desktop/Re-created jobspy project/Datasets/all_course_rankings_with_elective_core.csv'")
