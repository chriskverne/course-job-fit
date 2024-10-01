import pandas as pd
import spacy
import re

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')


# Function to clean text using SpaCy
def clean_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)


# List to store the extracted course data
courses_data_one = []  # with Pre reqs
courses_data = []  # without Pre reqs

# Read the text file
with open('courses_cleaned.txt', 'r') as file:
    content = file.read().strip()

# Split content into individual course entries
course_entries = content.split('\n\n')

# Collect all data in courses_data
for course in course_entries:
    lines = course.split('\n')
    for line in lines:
        course_name = line[0:9].strip()  # Extract course name
        description_one = line[9:].strip()  # Description with pre-reqs + all text after

        # Extract core level if present
        core_match = re.search(r'is_core=(\d)', description_one.lower())
        if core_match:
            is_core = int(core_match.group(1))
        else:
            is_core = None

        # Remove the is_core marker from the description
        description_one = re.sub(r'is_core=\d', '', description_one, flags=re.IGNORECASE).strip()

        courses_data_one.append((course_name, description_one, is_core))

        prereq_index = description_one.lower().find('prerequisite')  # Find index of prerequisite to be removed

        if prereq_index != -1:
            description_two = description_one[:prereq_index].strip()  # Description without pre-reqs
        else:
            description_two = description_one

        courses_data.append((course_name, description_two, is_core))

# removes first class which is ('ï»¿', '') due to the space character
courses_data.pop(0)

# Clean the course descriptions using SpaCy
cleaned_courses_data = [(course_name, clean_text(description), is_core) for course_name, description, is_core in
                        courses_data]

# Convert the cleaned data to a DataFrame
df = pd.DataFrame(cleaned_courses_data, columns=['course_name', 'filtered_description', 'is_core'])

# Export the DataFrame to an Excel file
excel_path = 'C:/Users/13054/Desktop/Re-created jobspy project/course_descriptions.xlsx'
df.to_excel(excel_path, index=False)

print("Data extracted and saved to", excel_path)
