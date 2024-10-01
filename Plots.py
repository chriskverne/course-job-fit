import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
from matplotlib.gridspec import GridSpec


# Load the data
all_courses_df = pd.read_csv('C:/Users/13054/Desktop/Re-created jobspy project/Datasets/all_course_rankings.csv')
core_courses_df = all_courses_df[all_courses_df['Is Core'].notna()]
elective_courses_df = all_courses_df[all_courses_df['Is Core'].isna()]

print(all_courses_df['Weighted Mean Salary'].quantile(0.25))
def add_legend(ax):
    legend_elements = [
        plt.Line2D([0], [0], color='green', lw=4, label='Core Classes'),
        plt.Line2D([0], [0], color='orange', lw=4, label='Elective Classes'),
        plt.Line2D([0], [0], color='red', lw=4, label='Elective + Core'),
        plt.Line2D([0], [0], color='blue', lw=4, label='Other Classes')
    ]
    ax.legend(handles=legend_elements, loc='upper left')

def get_bar_colors(df):
    return ['blue' if is_core else 'orange' for is_core in zip(df['Is Core'])]

# Two Metric Plots:
# Assign course type
def assign_course_type(row):
    if row['Is Core']:
        return 'Core'
    else:
        return 'Elective'

all_courses_df['Course Type'] = all_courses_df.apply(assign_course_type, axis=1)


def plot_average_similarity_distribution(df, bins=50):
    # Plot the data
    plt.figure(figsize=(12, 6))

    # Histogram
    sns.histplot(df['Average Similarity'], bins=bins, kde=True, stat="density", color="skyblue", edgecolor="black")

    # KDE plot
    sns.kdeplot(df['Average Similarity'], color='blue', linewidth=3)

    # Add titles and labels
    #plt.title('AS Distribution', fontsize=16)
    plt.xlabel('Average Similarity', fontsize=22)
    plt.ylabel('Frequency', fontsize=22)

    # Increase the size of the tick labels
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.grid(True)
    plt.show()

#plot_average_similarity_distribution(all_courses_df)

# Plot the relationship between average similarity and strong match count
def plot_similarity_vs_strong_matches(df, metric1, metric2):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=metric1, y=metric2, data=df, hue='Course Type', palette={'Core': 'green', 'Elective': 'orange', 'Both': 'red', 'Other': 'blue'}, edgecolor='black')
    plt.title('Average Similarity vs Strong-High Match Count')
    plt.xlabel('Average Similarity')
    plt.ylabel('Strong-High Match Count')
    plt.grid(True)
    plt.legend(title='Course Type')
    plt.show()


# Single Metric Distribution Plots:
import matplotlib.pyplot as plt

def plot_average_metric_barchart_side_by_side(elective_courses_df, core_courses_df):
    metrics = ['Average Similarity', 'Weighted Mean Salary', 'Strong Match Count', 'Strong-High Match Count']
    metric_labels = ['AS', 'WS', 'SMC', 'SHMC']

    fig = plt.figure(figsize=(10, 2))
    gs = GridSpec(1, 4, figure=fig, wspace=0.55)  # Adjust wspace to control spacing

    for i, (metric, metric_label) in enumerate(zip(metrics, metric_labels)):
        ax = fig.add_subplot(gs[i])
        avg_metric_electives = elective_courses_df[metric].mean()
        avg_metric_core = core_courses_df[metric].mean()

        std_metric_electives = elective_courses_df[metric].std()
        std_metric_core = core_courses_df[metric].std()

        categories = ['Elective', 'Core']
        averages = [avg_metric_electives, avg_metric_core]
        std_devs = [std_metric_electives, std_metric_core]

        colors = ['orange', 'green']
        ax.bar(categories, averages, yerr=std_devs, color=colors, edgecolor='black', capsize=5)
        ax.set_title(f'Average {metric_label}', fontsize=22)

        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)

        ax.grid(True)

    plt.tight_layout()
    plt.show()
plot_average_metric_barchart_side_by_side(elective_courses_df, core_courses_df)



def plot_weighted_mean_salary_distribution(df, salary_threshold=100000):
    # Sort the courses by Weighted Mean Salary
    sorted_df = df.sort_values(by='Weighted Mean Salary').reset_index(drop=True)

    # Calculate the percentage of courses
    sorted_df['Percentage'] = (sorted_df.index + 1) / len(sorted_df) * 100

    # Plot the data
    plt.figure(figsize=(12, 6))

    # Plot the weighted mean salary
    plt.plot(sorted_df['Percentage'], sorted_df['Weighted Mean Salary'], label='Weighted Mean Salary', color='blue', linewidth=4)

    # Add a horizontal line for the salary threshold
    plt.axhline(y=salary_threshold, color='r', linestyle='--', label=f'Salary Threshold: ${salary_threshold}', linewidth=4)

    # Find the percentage of courses above the salary threshold
    percentage_above_threshold = sorted_df[sorted_df['Weighted Mean Salary'] >= salary_threshold]['Percentage'].min()

    # Add a vertical line at the percentage threshold
    plt.axvline(x=percentage_above_threshold, color='g', linestyle='--',
                label=f'{100 - percentage_above_threshold:.1f}% of courses above ${salary_threshold}', linewidth=4)

    # Add titles and labels
    # plt.title('WS Distribution', fontsize=16)
    plt.xlabel('Percentage of Courses (%)', fontsize=22)
    plt.ylabel('Weighted Salary ($)', fontsize=22)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # plt.legend() # Small box left corner
    plt.grid(True)
    plt.show()

#plot_weighted_mean_salary_distribution(all_courses_df)

def plot_strong_matches_distribution(df):
    # Sort the courses by Strong Match Count
    sorted_df = df.sort_values(by='Strong Match Count').reset_index(drop=True)

    # Calculate the percentage of courses
    sorted_df['Percentage'] = (sorted_df.index + 1) / len(sorted_df) * 100

    # Calculate the sum of SMC for the top 50%
    mid_point = len(sorted_df) // 2
    top_50_sum = sorted_df.iloc[:mid_point]['Strong Match Count'].sum()
    total_smc = sorted_df['Strong Match Count'].sum()

    # Calculate the percentage of SMC that the top 50% have
    top_50_percentage = (top_50_sum / total_smc) * 100

    # Plot the data
    plt.figure(figsize=(12, 6))

    # Plot the strong match count
    plt.plot(sorted_df['Percentage'], sorted_df['Strong Match Count'], color='blue', linewidth=4)

    # Shade the area under the curve for the top 50%
    plt.fill_between(sorted_df['Percentage'][:mid_point], sorted_df['Strong Match Count'][:mid_point], color='green', alpha=0.3)

    # Shade the area under the curve for the bottom 50%
    plt.fill_between(sorted_df['Percentage'][mid_point:], sorted_df['Strong Match Count'][mid_point:], color='orange', alpha=0.3)

    # Add a vertical line at the 50% mark
    plt.axvline(x=50, color='g', linestyle='--', linewidth=4, label=f'Top 50% have {100 - top_50_percentage:.1f}% of SMC')

    # Add a horizontal line for the match threshold

    # Add titles and labels
    # plt.title('SMC Distribution', fontsize=16)
    plt.xlabel('Percentage of Courses (%)', fontsize=22)
    plt.ylabel('Strong Match Count', fontsize=22)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    #plt.legend()
    plt.grid(True)
    plt.show()


#plot_strong_matches_distribution(all_courses_df)



def plot_strong_high_matches_distribution(df):
    # Sort the courses by Strong-High Match Count
    sorted_df = df.sort_values(by='Strong-High Match Count').reset_index(drop=True)

    # Calculate the percentage of courses
    sorted_df['Percentage'] = (sorted_df.index + 1) / len(sorted_df) * 100

    # Calculate the sum of SHMC for the top 50%
    mid_point = len(sorted_df) // 2
    top_50_sum = sorted_df.iloc[:mid_point]['Strong-High Match Count'].sum()
    total_shmc = sorted_df['Strong-High Match Count'].sum()

    # Calculate the percentage of SHMC that the top 50% have
    top_50_percentage = (top_50_sum / total_shmc) * 100

    # Plot the data
    plt.figure(figsize=(12, 6))

    # Plot the strong-high match count
    plt.plot(sorted_df['Percentage'], sorted_df['Strong-High Match Count'], color='blue', linewidth=4)

    # Shade the area under the curve for the top 50%
    plt.fill_between(sorted_df['Percentage'][:mid_point], sorted_df['Strong-High Match Count'][:mid_point], color='green', alpha=0.3)

    # Shade the area under the curve for the bottom 50%
    plt.fill_between(sorted_df['Percentage'][mid_point:], sorted_df['Strong-High Match Count'][mid_point:], color='orange', alpha=0.3)

    # Add a vertical line at the 50% mark
    plt.axvline(x=50, color='g', linestyle='--', linewidth=4) #, label=f'Top 50% have {100-top_50_percentage:.1f}% of SHMC'

    # Add titles and labels
    #plt.title('SHMC Distribution', fontsize=16)
    plt.xlabel('Percentage of Courses (%)', fontsize=22)
    plt.ylabel('Strong-High Match Count', fontsize=22)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.legend()
    plt.grid(True)
    plt.show()

#plot_strong_high_matches_distribution(all_courses_df)


def show_distribution_plots(df, bins=50):
    plot_average_similarity_distribution(df, bins)
    plot_weighted_mean_salary_distribution(df, bins)
    plot_strong_match_distribution(df, bins)
    plot_strong_high_match_distribution(df, bins)

# Courses Ranked Plots
def plot_top_courses_by_salary(df, title, top_n=10):
    top_courses = df.nlargest(top_n, 'Weighted Mean Salary')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_courses['Course Name'], top_courses['Weighted Mean Salary'], color='blue', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Weighted Mean Salary')
    ax.set_ylabel('Course Name')
    ax.invert_yaxis()
    ax.grid(True)
    plt.show()

def plot_top_courses_by_strong_high_matches(df, title ,top_n=10):
    top_courses = df.nlargest(top_n, 'Strong-High Match Count')
    colors = get_bar_colors(top_courses)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_courses['Course Name'], top_courses['Strong-High Match Count'], color=colors, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Strong-High Match Count')
    ax.set_ylabel('Course Name')
    ax.invert_yaxis()
    ax.grid(True)
    add_legend(ax)
    plt.show()

def plot_top_courses_by_similarity(df, title ,top_n=10):
    top_courses = df.nlargest(top_n, 'Average Similarity')
    colors = get_bar_colors(top_courses)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_courses['Course Name'], top_courses['Average Similarity'], color=colors, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Average Similarity')
    ax.set_ylabel('Course Name')
    ax.invert_yaxis()
    ax.grid(True)
    add_legend(ax)
    plt.show()
def plot_top_courses_by_strong_matches(df, title ,top_n=10):
    top_courses = df.nlargest(top_n, 'Strong Match Count')
    colors = get_bar_colors(top_courses)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_courses['Course Name'], top_courses['Strong Match Count'], color=colors, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel('Strong Match Count')
    ax.set_ylabel('Course Name')
    ax.invert_yaxis()
    ax.grid(True)
    add_legend(ax)
    plt.show()

def show_top_course_rankings(df,title, top_n=10):
    plot_top_courses_by_salary(df,title + 'Salary',top_n=top_n)
    plot_top_courses_by_strong_high_matches(df, title + 'Strong-High Matches', top_n=top_n)
    plot_top_courses_by_similarity(df, title + 'Average Similarity' ,top_n=top_n)
    plot_top_courses_by_strong_matches(df, title + 'Strong Matches' ,top_n=top_n)
def plot_bottom_courses_by_salary(df, bottom_n=10):
    bottom_courses = df.nsmallest(bottom_n, 'Weighted Mean Salary')
    colors = get_bar_colors(bottom_courses)
    plt.figure(figsize=(10, 6))
    plt.barh(bottom_courses['Course Name'], bottom_courses['Weighted Mean Salary'], color=colors, edgecolor='black')
    plt.title(f'Bottom {bottom_n} Courses by Weighted Mean Salary')
    plt.xlabel('Weighted Mean Salary')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    add_legend(plt.gca())
    plt.show()

def plot_bottom_courses_by_strong_high_matches(df, bottom_n=10):
    bottom_courses = df.nsmallest(bottom_n, 'Strong-High Match Count')
    colors = get_bar_colors(bottom_courses)
    plt.figure(figsize=(10, 6))
    plt.barh(bottom_courses['Course Name'], bottom_courses['Strong-High Match Count'], color=colors, edgecolor='black')
    plt.title(f'Bottom {bottom_n} Courses by Strong-High Match Count')
    plt.xlabel('Strong-High Match Count')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    add_legend(plt.gca())
    plt.show()

def plot_bottom_courses_by_similarity(df, bottom_n=10):
    bottom_courses = df.nsmallest(bottom_n, 'Average Similarity')
    colors = get_bar_colors(bottom_courses)
    plt.figure(figsize=(10, 6))
    plt.barh(bottom_courses['Course Name'], bottom_courses['Average Similarity'], color=colors, edgecolor='black')
    plt.title(f'Bottom {bottom_n} Courses by Average Similarity')
    plt.xlabel('Average Similarity')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    add_legend(plt.gca())
    plt.show()

def plot_bottom_courses_by_strong_matches(df, bottom_n=10):
    bottom_courses = df.nsmallest(bottom_n, 'Strong Match Count')
    colors = get_bar_colors(bottom_courses)
    plt.figure(figsize=(10, 6))
    plt.barh(bottom_courses['Course Name'], bottom_courses['Strong Match Count'], color=colors, edgecolor='black')
    plt.title(f'Bottom {bottom_n} Courses by Strong Match Count')
    plt.xlabel('Strong Match Count')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    add_legend(plt.gca())
    plt.show()

def show_bottom_course_rankings(df, bottom_n=10):
    plot_bottom_courses_by_salary(df, bottom_n=bottom_n)
    #plot_bottom_courses_by_strong_high_matches(df, bottom_n=10)
    plot_bottom_courses_by_similarity(df, bottom_n=bottom_n)
    #plot_bottom_courses_by_strong_matches(df, bottom_n=10)

def plot_top_combined_rank(df,title,top_n=10):
    # Top 10 courses
    top_courses = df.nsmallest(top_n, 'Combined Rank')
    plt.figure(figsize=(10, 6))
    plt.barh(top_courses['Course Name'], top_courses['Combined Rank'], color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel('Combined Rank')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()

def plot_bottom_combined_rank(df, bottom_n=10):
    # Bottom 10 courses
    bottom_courses = df.nlargest(bottom_n, 'Combined Rank').sort_values(by='Combined Rank', ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(bottom_courses['Course Name'], bottom_courses['Combined Rank'], color='salmon', edgecolor='black')
    plt.title(f'Bottom {bottom_n} Courses by Combined Rank')
    plt.xlabel('Combined Rank')
    plt.ylabel('Course Name')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()

def plot_course_comparison_histogram(all_courses_df, elective_courses_df, core_courses_df, metric, metric_label):
    plt.figure(figsize=(10, 6))
    # Plot histogram for all courses
    plt.hist(all_courses_df[metric], bins=50, color='skyblue', edgecolor='black', alpha=0.5, label='All Courses')
    # Plot histogram for electives
    plt.hist(elective_courses_df[metric], bins=50, color='orange', edgecolor='black', alpha=0.5, label='Electives')
    # Plot histogram for core courses
    plt.hist(core_courses_df[metric], bins=50, color='green', edgecolor='black', alpha=0.5, label='Core Courses')
    plt.title(f'Distribution of {metric_label}')
    plt.xlabel(metric_label)
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()


def cor_matrix():
    metric_labels = ['Rank Average Similarity', 'Rank Weighted Mean Salary', 'Rank Strong Match Count',
                     'Rank Strong-High Match Count']
    # Create a DataFrame with only the selected metrics
    metrics_df = all_courses_df[metric_labels]

    # Calculate the correlation matrix
    correlation_matrix = metrics_df.corr()

    # Custom labels
    custom_labels = ['AS', 'WS', 'SMC', 'SHMC']

    # Plot the correlation matrix
    plt.figure(figsize=(6, 4))
    ax = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', annot_kws={"size": 10},
                     xticklabels=custom_labels, yticklabels=custom_labels)
    plt.title('Course Ranking Relation', fontsize=14)
    plt.xticks(fontsize=10, rotation=0)
    plt.yticks(fontsize=10, rotation=0)
    plt.show()

#cor_matrix()
# Plot comparison histograms
#plot_course_comparison_histogram(all_courses_df, elective_courses_df, core_courses_df, 'Average Similarity', 'Average Similarity')
#plot_course_comparison_histogram(all_courses_df, elective_courses_df, core_courses_df, 'Weighted Mean Salary', 'Weighted Mean Salary')
#plot_course_comparison_histogram(all_courses_df, elective_courses_df, core_courses_df, 'Strong-High Match Count', 'Strong-High Match Count')

#show_distribution_plots(all_courses_df, 50)
#show_top_course_rankings(all_courses_df, 'Top 20 Courses By ',top_n=20)
#show_bottom_course_rankings(all_courses_df, 20)
#plot_top_combined_rank(all_courses_df, 'Top 10 Courses By Combined Rank')
#plot_bottom_combined_rank(all_courses_df)

#show_distribution_plots(elective_courses_df)
#show_top_course_rankings(elective_courses_df,'Electives Ranked By ',top_n=31)
#plot_top_combined_rank(elective_courses_df,'Elective Courses By Combined Rank' ,top_n=31)

#show_distribution_plots(core_courses_df)
#show_top_course_rankings(core_courses_df, 'Core Courses Ranked By ', top_n=14)
#plot_top_combined_rank(core_courses_df, 'Core Courses Ranked By Combined Rank', top_n=14)

# Plot the average metric bar charts WORKS


#plot_average_metric_barchart_side_by_side(elective_courses_df, core_courses_df)

#print(core_courses_df)
#plot_similarity_vs_strong_matches(all_courses_df, 'Average Similarity', 'Strong Match Count')
#plot_similarity_vs_strong_matches(all_courses_df, 'Average Similarity', 'Strong-High Match Count')
#plot_similarity_vs_strong_matches(all_courses_df, 'Average Similarity', 'Weighted Mean Salary')

num_of_jobs = 431
num_of_high_paying_jobs = 349
#plot_weighted_mean_salary_distribution(all_courses_df, 100000)
#plot_strong_high_matches_distribution(all_courses_df,math.floor(num_of_high_paying_jobs/2))
#plot_strong_matches_distribution(all_courses_df, math.floor(num_of_jobs/2))