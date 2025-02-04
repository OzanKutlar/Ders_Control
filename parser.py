import pandas as pd
import re
import os
import json

# File paths
input_file = 'data.txt'
output_file = 'course_data.json'

# Read data from the text file with UTF-8 encoding
with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

# Split data into blocks by double newline
blocks = re.split(r'\n\s*\n+', data.strip())

# Initialize list to store course data
courses = []

# Process the data in chunks of 8 lines
for i in range(0, len(blocks), 8):
    course = {
        "Course Code": blocks[i + 0] if len(blocks) > i + 0 else '',
        "Course Name": blocks[i + 1] if len(blocks) > i + 1 else '',
        "Section": blocks[i + 2] if len(blocks) > i + 2 else '',
        "Full Course Name": blocks[i + 3] if len(blocks) > i + 3 else '',
        "Instructor": blocks[i + 4] if len(blocks) > i + 4 else '',
        "Schedule": blocks[i + 5] if len(blocks) > i + 5 else '',
        "Location": blocks[i + 6] if len(blocks) > i + 6 else '',
        "Capacity": blocks[i + 7] if len(blocks) > i + 7 else ''
    }
    courses.append(course)

# Check if the JSON file already exists
if os.path.exists(output_file):
    # If exists, load existing data and append new courses
    with open(output_file, 'r', encoding='utf-8') as file:
        existing_courses = json.load(file)
    
    existing_courses.extend(courses)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(existing_courses, file, indent=4, ensure_ascii=False)
    
    print(f"Data successfully processed and appended to '{output_file}'.")
else:
    # If not exists, create a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(courses, file, indent=4, ensure_ascii=False)

    print(f"Data successfully processed and saved to '{output_file}'.")
