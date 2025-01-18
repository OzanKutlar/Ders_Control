import pandas as pd
import re
import sys


eklenenDersFile = 'eklenenders.csv'

def parse_schedule(course_code, course_name, schedule):
    # Define a regular expression pattern to match day and time period
    if isinstance(schedule, float):
        # print(f"Skipping schedule for {course_code} - {course_name} (No schedule available)")
        return None
        
    # print(f"Parsing schedule for {course_code} - {course_name}...")
        
        
    pattern = r'(\w+)\s*:\s*(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})'
    # Find all matches in the schedule string
    matches = re.findall(pattern, schedule)
    return matches
    
def initialize_weekly_schedule():
    # Initialize a weekly schedule with empty lists for each day
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
    # days = ['MON', 'TUE', 'WED', 'FRI']
    weekly_schedule = {day: [] for day in days}
    return weekly_schedule

def time_overlap(time1, time2):
    start1, end1 = map(pd.to_datetime, time1.split(' - '))
    start2, end2 = map(pd.to_datetime, time2.split(' - '))
    return not (end1 <= start2 or end2 <= start1)

def add_classes_to_schedule(weekly_schedule, location, course_code, course_name, day, time_period):
    class_entry = f'{course_code} - {course_name} - {location}: {time_period}'
    weekly_schedule[day].append(class_entry)
    # return True
    
def checkClasses(weekly_schedule, course_code, course_name, day, time_period):
    # Format the entry with course code and name
    # class_entry = f'{course_code} - {course_name}: {time_period}'
    
    # Check for time slot availability
    for existing_entry in weekly_schedule[day]:
        existing_time_period = existing_entry.split(': ')[-1]
        if time_overlap(existing_time_period, time_period):
            # print(f'Conflict: {class_entry} cannot be scheduled due to overlap with existing class at {day}.')
            return False
    
    # weekly_schedule[day].append(class_entry)
    return True

def main():
    # Load the CSV file into a DataFrame
    target = ''
    if len(sys.argv) < 2:
        target = 'course_data.csv'
    else:    
        target = sys.argv[1]
    
    
    print(f'Reading data from {target}')
    
    eklenenDers = pd.read_csv(eklenenDersFile)
    
    weekly_schedule = initialize_weekly_schedule()
    
    for i, row in eklenenDers.iterrows():
        course_code = row['Section']
        course_name = row['Course Name']
        schedule = row['Schedule']
        location = row['Location']
        
        # Extract schedule details
        schedule_details = parse_schedule(course_code, course_name, schedule)
        
        if(schedule_details == None):
            continue
        
        for day, time_period in schedule_details:
            if day in weekly_schedule:
                add_classes_to_schedule(weekly_schedule, location, course_code, course_name, day, time_period)
        
    
    df = pd.read_csv(target)
    
    # Iterate over each row in the DataFrame
    for i, row in df.iterrows():
        course_code = row['Section']
        course_name = row['Course Name']
        schedule = row['Schedule']
        location = row['Location']
        
        # Extract schedule details
        schedule_details = parse_schedule(course_code, course_name, schedule)
        
        if(schedule_details == None):
            continue
        
        doesFit = True
        for day, time_period in schedule_details:
            if day in weekly_schedule:
                if not checkClasses(weekly_schedule, course_code, course_name, day, time_period):
                    doesFit = False
            else:
                doesFit = False
            # print(f'Attempting to add Day: {day}, Time Period: {time_period}')
        if doesFit:
            print(f'Found class {course_code} - {course_name} - {location} : ')
            for day, time_period in schedule_details:
                print(f'  - {day} : {time_period}')
            
    for day, time_slots in weekly_schedule.items():
        print(f'{day}:')
        if time_slots:
            for time_slot in time_slots:
                print(f'  {time_slot}')
        else:
            print('  No classes')

if __name__ == "__main__":
    main()
