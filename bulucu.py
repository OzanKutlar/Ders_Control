import json
import re
import sys
import pandas as pd

eklenenDersFile = 'eklenenders.json'  # JSON file containing pre-scheduled classes


def parse_schedule(course_code, course_name, schedule):
    if isinstance(schedule, float):  # Handle missing schedule values
        return None

    pattern = r'(\w+)\s*:\s*(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})'
    matches = re.findall(pattern, schedule)
    return matches


def initialize_weekly_schedule():
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
    return {day: [] for day in days}


def time_overlap(time1, time2):
    start1, end1 = map(pd.to_datetime, time1.split(' - '))
    start2, end2 = map(pd.to_datetime, time2.split(' - '))
    return not (end1 <= start2 or end2 <= start1)


def add_classes_to_schedule(weekly_schedule, location, course_code, course_name, day, time_period):
    class_entry = f'{course_code} - {course_name} - {location}: {time_period}'
    weekly_schedule[day].append(class_entry)


def check_classes(weekly_schedule, course_code, course_name, day, time_period):
    for existing_entry in weekly_schedule[day]:
        existing_time_period = existing_entry.split(': ')[-1]
        if time_overlap(existing_time_period, time_period):
            return False
    return True


def main():
    target = 'course_data.json' if len(sys.argv) < 2 else sys.argv[1]
    print(f'Reading data from {target}')

    # Load JSON file
    with open(eklenenDersFile, 'r', encoding='utf-8') as file:
        eklenenDers = json.load(file)

    weekly_schedule = initialize_weekly_schedule()

    # Load existing scheduled classes
    for row in eklenenDers:
        course_code = row['Section']
        course_name = row['Course Name']
        schedule = row['Schedule']
        location = row['Location']

        schedule_details = parse_schedule(course_code, course_name, schedule)
        if schedule_details is None:
            continue

        for day, time_period in schedule_details:
            if day in weekly_schedule:
                add_classes_to_schedule(weekly_schedule, location, course_code, course_name, day, time_period)

    # Load new courses to check availability
    with open(target, 'r', encoding='utf-8') as file:
        df = json.load(file)

    for row in df:
        course_code = row['Section']
        course_name = row['Course Name']
        schedule = row['Schedule']
        location = row['Location']

        schedule_details = parse_schedule(course_code, course_name, schedule)
        if schedule_details is None:
            continue

        does_fit = all(
            check_classes(weekly_schedule, course_code, course_name, day, time_period)
            for day, time_period in schedule_details if day in weekly_schedule
        )

        if does_fit:
            print(f'Found class {course_code} - {course_name} - {location}:')
            for day, time_period in schedule_details:
                print(f'  - {day} : {time_period}')

    # Print the weekly schedule
    for day, time_slots in weekly_schedule.items():
        print(f'{day}:')
        if time_slots:
            for time_slot in time_slots:
                print(f'  {time_slot}')
        else:
            print('  No classes')


if __name__ == "__main__":
    main()
