import pandas as pd
import re
import os

# File paths
input_file = 'data.txt'
output_file = 'course_data.csv'

# Read data from the text file with UTF-8 encoding
with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

# Split data into blocks by double newline
blocks = re.split(r'\n\s*\n+', data.strip())

# Initialize lists to store the data
course_codes = []
course_names = []
sections = []
full_names = []
instructors = []
schedules = []
locations = []
capacities = []

for i in range(0, len(blocks), 8):
    course_codes.append(blocks[i + 0] if len(blocks) > i + 0 else '')
    course_names.append(blocks[i + 1] if len(blocks) > i + 1 else '')
    sections.append(blocks[i + 2] if len(blocks) > i + 2 else '')
    full_names.append(blocks[i + 3] if len(blocks) > i + 3 else '')
    instructors.append(blocks[i + 4] if len(blocks) > i + 4 else '')
    schedules.append(blocks[i + 5] if len(blocks) > i + 5 else '')
    locations.append(blocks[i + 6] if len(blocks) > i + 6 else '')
    capacities.append(blocks[i + 7] if len(blocks) > i + 7 else '')

# Create a DataFrame
df = pd.DataFrame({
    'Course Code': course_codes,
    'Course Name': course_names,
    'Section': sections,
    'Full Course Name': full_names,
    'Instructor': instructors,
    'Schedule': schedules,
    'Location': locations,
    'Capacity': capacities
})

# Check if the CSV file already exists
if os.path.exists(output_file):
    # If exists, append to it
    df_existing = pd.read_csv(output_file, encoding='utf-8-sig')
    df_combined = pd.concat([df_existing, df], ignore_index=True)
    df_combined.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Data successfully processed and appended to '{output_file}'.")
else:
    # If not exists, create a new file
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Data successfully processed and saved to '{output_file}'.")