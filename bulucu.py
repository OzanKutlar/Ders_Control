import json
import re
import sys
import pandas as pd

eklenenDersFile = 'eklenenders.json'  # JSON file containing scheduled classes


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


def display_class_details(class_data):
    """Display class details in a readable format."""
    print("\n--- Class Details ---")
    print(f"Section: {class_data['Section']}")
    print(f"Course Name: {class_data['Course Name']}")
    print(f"Schedule: {class_data['Schedule']}")
    print(f"Location: {class_data['Location']}")
    print("---------------------")


def save_updated_schedule(eklenenDers):
    """Save the updated schedule back to eklenenders.json."""
    with open(eklenenDersFile, 'w', encoding='utf-8') as file:
        json.dump(eklenenDers, file, indent=4)
    print("\n✅ Class added to schedule successfully!\n")


def main():
    target = 'course_data.json' if len(sys.argv) < 2 else sys.argv[1]
    print(f'Reading data from {target}')

    # Load scheduled classes
    with open(eklenenDersFile, 'r', encoding='utf-8') as file:
        eklenenDers = json.load(file)

    weekly_schedule = initialize_weekly_schedule()

    # Add existing scheduled classes to the weekly schedule
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

    # Load available classes
    with open(target, 'r', encoding='utf-8') as file:
        df = json.load(file)

    available_classes = []

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
            available_classes.append(row)

    if not available_classes:
        print("\n❌ No available classes that fit the current schedule.")
        return

    print("\n📚 Available Classes:\n")
    for idx, class_data in enumerate(available_classes, start=1):
        print(f"{idx}. {class_data['Section']} - {class_data['Course Name']} ({class_data['Schedule']})")

    while True:
        try:
            choice = input("\nEnter the number of the class to view details (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                print("\nExiting selection process.\n")
                break

            choice = int(choice)
            if 1 <= choice <= len(available_classes):
                selected_class = available_classes[choice - 1]
                display_class_details(selected_class)

                confirm = input("\nDo you want to add this class to the schedule? (y/n): ").strip().lower()
                if confirm == 'y':
                    eklenenDers.append(selected_class)
                    save_updated_schedule(eklenenDers)

                    # Update the weekly schedule dynamically
                    schedule_details = parse_schedule(selected_class['Section'], selected_class['Course Name'], selected_class['Schedule'])
                    for day, time_period in schedule_details:
                        if day in weekly_schedule:
                            add_classes_to_schedule(weekly_schedule, selected_class['Location'], selected_class['Section'], selected_class['Course Name'], day, time_period)

                    print(f"✅ {selected_class['Section']} has been added to the schedule.\n")

                else:
                    print("❌ Class was not added.\n")
            else:
                print("⚠️ Invalid choice. Please enter a valid number.")

        except ValueError:
            print("⚠️ Invalid input. Please enter a number or 'q' to quit.")

    # Print updated weekly schedule
    print("\n📅 Updated Weekly Schedule:\n")
    for day, time_slots in weekly_schedule.items():
        print(f'{day}:')
        if time_slots:
            for time_slot in time_slots:
                print(f'  {time_slot}')
        else:
            print('  No classes')


if __name__ == "__main__":
    main()
