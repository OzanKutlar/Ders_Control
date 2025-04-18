import os
import json
import glob
from datetime import datetime
import shutil

def get_download_folder():
    """Return the default downloads path for Windows."""
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def find_json_files_in_downloads():
    """Find all JSON files in the downloads folder."""
    download_folder = get_download_folder()
    json_files = glob.glob(os.path.join(download_folder, '*.json'))
    return json_files

def find_json_files_in_current_directory():
    """Find all JSON files in the current directory."""
    json_files = glob.glob('*.json')
    return json_files

def parse_timeslots(timeslots):
    """Parse timeslots into a structured format."""
    parsed_slots = []
    for slot in timeslots:
        day, time_range = slot.split(' : ')
        start_time, end_time = time_range.split(' - ')
        
        # Convert times to datetime objects for easier comparison
        start_dt = datetime.strptime(start_time, '%H:%M')
        end_dt = datetime.strptime(end_time, '%H:%M')
        
        parsed_slots.append({
            'day': day.strip(),
            'start': start_dt,
            'end': end_dt,
            'original': slot
        })
    return parsed_slots

def has_conflict(existing_timeslots, new_timeslots):
    """Check if there's a scheduling conflict between existing and new timeslots."""
    for new_slot in new_timeslots:
        for exist_slot in existing_timeslots:
            if new_slot['day'] == exist_slot['day']:
                # Check for overlap
                if (new_slot['start'] <= exist_slot['end'] and 
                    new_slot['end'] >= exist_slot['start']):
                    return True
    return False

def create_new_selected_file(filename):
    """Create a new selected courses file."""
    data = {
        "selected_courses": []
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return data

def format_course_info(course):
    """Format course information for display."""
    return f"{course[0]} - {course[1]} - {course[2]} - {course[4]}"

def main():
    print("Lesson Selection Program")
    print("=======================")
    
    # Find JSON files in downloads folder
    download_json_files = find_json_files_in_downloads()
    
    # Check if any JSON files were found
    if not download_json_files:
        print("No JSON files found in your downloads folder.")
        input_choice = None
    else:
        print("\nAvailable JSON files in downloads folder:")
        for i, file_path in enumerate(download_json_files, 1):
            print(f"{i}. {os.path.basename(file_path)}")
        
        print("\nWhich file contains the course listings?")
        selection = input("Enter number (or press Enter to skip): ")
        
        if selection.strip() and selection.isdigit() and 1 <= int(selection) <= len(download_json_files):
            input_choice = download_json_files[int(selection) - 1]
        else:
            input_choice = None
            print("No valid selection. Proceeding without input file.")
    
    # Load available courses if an input file was selected
    available_courses = []
    if input_choice:
        try:
            with open(input_choice, 'r') as f:
                available_courses = json.load(f)
            print(f"Loaded {len(available_courses)} courses from {os.path.basename(input_choice)}")
        except Exception as e:
            print(f"Error loading file: {e}")
            available_courses = []
    
    # Find JSON files in current directory for selected courses
    current_json_files = find_json_files_in_current_directory()
    
    if not current_json_files:
        print("\nNo selected courses file found in current directory.")
        filename = input("Enter a name for your new selected courses file (e.g., my_courses.json): ")
        if not filename.endswith('.json'):
            filename += '.json'
        selected_data = create_new_selected_file(filename)
        print(f"Created new file: {filename}")
    else:
        print("\nExisting course files in current directory:")
        for i, file_path in enumerate(current_json_files, 1):
            print(f"{i}. {file_path}")
        print(f"{len(current_json_files) + 1}. Create a new file")
        
        selection = input("Enter number for your selected courses file: ")
        
        if selection.isdigit():
            selection = int(selection)
            if 1 <= selection <= len(current_json_files):
                selected_file = current_json_files[selection - 1]
                try:
                    with open(selected_file, 'r') as f:
                        selected_data = json.load(f)
                    print(f"Loaded selected courses from {selected_file}")
                except Exception as e:
                    print(f"Error loading file: {e}")
                    selected_file = input("Enter a name for your new selected courses file: ")
                    if not selected_file.endswith('.json'):
                        selected_file += '.json'
                    selected_data = create_new_selected_file(selected_file)
            else:
                selected_file = input("Enter a name for your new selected courses file: ")
                if not selected_file.endswith('.json'):
                    selected_file += '.json'
                selected_data = create_new_selected_file(selected_file)
        else:
            selected_file = input("Enter a name for your new selected courses file: ")
            if not selected_file.endswith('.json'):
                selected_file += '.json'
            selected_data = create_new_selected_file(selected_file)
    
    # Ensure selected_courses exists in the data
    if "selected_courses" not in selected_data:
        selected_data["selected_courses"] = []
    
    # Create timetable from selected courses
    timetable = []
    for course in selected_data["selected_courses"]:
        timeslots = parse_timeslots(course[3])
        for slot in timeslots:
            timetable.append(slot)
    
    # Display current timetable
    if timetable:
        print("\nCurrent Timetable:")
        for i, course in enumerate(selected_data["selected_courses"], 1):
            print(f"{i}. {format_course_info(course)}")
            for slot in course[3]:
                print(f"   {slot}")
    else:
        print("\nYour timetable is currently empty.")
    
    # Find courses that fit into the current schedule
    if available_courses:
        print("\nAvailable courses that fit your schedule:")
        fitting_courses = []
        
        for course in available_courses:
            course_timeslots = parse_timeslots(course[3])
            if not has_conflict(timetable, course_timeslots):
                fitting_courses.append(course)
                
        if not fitting_courses:
            print("No courses found that fit your current schedule.")
        else:
            for i, course in enumerate(fitting_courses, 1):
                print(f"{i}. {format_course_info(course)}")
                for slot in course[3]:
                    print(f"   {slot}")
            
            # Let user select a course to add
            selection = input("\nEnter number to add a course (or press Enter to skip): ")
            if selection.strip() and selection.isdigit() and 1 <= int(selection) <= len(fitting_courses):
                selected_course = fitting_courses[int(selection) - 1]
                selected_data["selected_courses"].append(selected_course)
                print(f"Added course: {selected_course[1]}")
                
                # Save updated selected courses
                with open(selected_file, 'w') as f:
                    json.dump(selected_data, f, indent=2)
                print(f"Updated {selected_file} with new course selection.")
    
    # Ask if user wants to delete the input file
    if input_choice:
        delete_choice = input(f"\nDelete input file {os.path.basename(input_choice)}? [y/N]: ")
        if delete_choice.lower() == 'y':
            try:
                os.remove(input_choice)
                print(f"Deleted {os.path.basename(input_choice)}")
            except Exception as e:
                print(f"Error deleting file: {e}")
        else:
            print("Input file kept.")

if __name__ == "__main__":
    main()