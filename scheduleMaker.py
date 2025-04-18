import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import TABLEAU_COLORS
import re
from datetime import datetime, timedelta
import math

def find_json_files():
    """Find all JSON files in the current directory."""
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    return json_files

def select_json_file(json_files):
    """Let the user select a JSON file from the list."""
    if not json_files:
        print("No JSON files found in the current directory.")
        return None
    
    print("Available JSON files:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")
    
    try:
        selection = int(input("Enter the number of the file you want to use: "))
        if 1 <= selection <= len(json_files):
            return json_files[selection - 1]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Please enter a valid number.")
        return None

def parse_time_slot(time_slot):
    """Parse a time slot string like 'MON : 09:00 - 10:50' into day, start time, and end time."""
    pattern = r'([A-Z]+)\s*:\s*(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})'
    match = re.match(pattern, time_slot)
    
    if match:
        day, start_time, end_time = match.groups()
        return day, start_time, end_time
    return None, None, None

def round_up_to_half_hour(time_str):
    """Round up the time to the nearest half hour."""
    time_obj = datetime.strptime(time_str, '%H:%M')
    
    # Get minutes
    minutes = time_obj.minute
    
    # Round up to nearest half hour
    if minutes > 0 and minutes <= 30:
        time_obj = time_obj.replace(minute=30)
    elif minutes > 30:
        # Round up to the next hour
        time_obj = time_obj + timedelta(hours=1)
        time_obj = time_obj.replace(minute=0)
    
    return time_obj.strftime('%H:%M')

def time_to_position(time_str):
    """Convert time string like '09:00' to a position on the y-axis."""
    time_obj = datetime.strptime(time_str, '%H:%M')
    
    # Base time is 9:00 AM
    base_time = datetime.strptime('09:00', '%H:%M')
    
    # Calculate the difference in minutes
    diff_minutes = (time_obj - base_time).total_seconds() / 60
    
    # Return the position (1 hour = 1 unit on the y-axis)
    return diff_minutes / 60

def day_to_position(day):
    """Convert day string to position on the x-axis."""
    days = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
    return days.get(day, -1)

def draw_timetable(courses_data):
    """Draw the timetable using matplotlib."""
    # Set up the figure
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Set up the timetable grid
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = list(range(9, 19))  # 9 AM to 6 PM
    
    # Draw grid
    for i in range(len(days) + 1):
        ax.axvline(i, color='gray', linestyle='-', alpha=0.3)
    
    for i in range(len(hours) + 1):
        ax.axhline(i, color='gray', linestyle='-', alpha=0.3)
    
    # Set labels
    ax.set_xticks([i + 0.5 for i in range(len(days))])
    ax.set_xticklabels(days)
    
    ax.set_yticks([i - 9 for i in range(9, 19)])
    ax.set_yticklabels([f"{h}:00" for h in hours])
    
    # Invert y-axis to have earliest time at the top
    ax.invert_yaxis()
    
    # Add half-hour markers
    for i in range(len(hours)):
        ax.axhline(i + 0.5, color='gray', linestyle='--', alpha=0.2)
        y_pos = i + 0.5
        ax.text(-0.5, y_pos, f"{hours[i]}:30", va='center', ha='right', fontsize=8)
    
    # Set up the colors for courses
    color_list = list(TABLEAU_COLORS.values())
    
    # Draw the courses
    for i, course in enumerate(courses_data["selected_courses"]):
        course_code = course[0]
        course_name = course[1]
        location = course[4]
        
        # Get a color for the course
        course_color = color_list[i % len(color_list)]
        
        # Process each time slot
        for time_slot in course[3]:
            day, start_time, end_time = parse_time_slot(time_slot)
            
            if day is None or start_time is None or end_time is None:
                continue
            
            # Skip slots that entirely occur before 9:00 AM
            start_time_obj = datetime.strptime(start_time, '%H:%M')
            if start_time_obj.hour < 9:
                # If the end time extends past 9:00 AM, adjust the start time to 9:00 AM
                end_time_obj = datetime.strptime(end_time, '%H:%M')
                if end_time_obj.hour >= 9 or (end_time_obj.hour == 8 and end_time_obj.minute > 0):
                    start_time = "09:00"
                else:
                    continue  # Skip this time slot entirely
            
            # Round up the end time to the nearest half hour
            end_time = round_up_to_half_hour(end_time)
            
            day_pos = day_to_position(day)
            start_pos = time_to_position(start_time)
            end_pos = time_to_position(end_time)
            
            if day_pos < 0:
                continue
                
            # Draw the course block
            rect = patches.Rectangle(
                (day_pos, start_pos), 1, end_pos - start_pos,
                linewidth=1, edgecolor='black', facecolor=course_color, alpha=0.7
            )
            ax.add_patch(rect)
            
            # Add text
            display_text = f"{course_code}\n{course_name}"
            if location != "NULL":
                display_text += f"\n{location}"
                
            ax.text(
                day_pos + 0.5, start_pos + (end_pos - start_pos)/2,
                display_text,
                ha='center', va='center', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3')
            )
    
    # Set title and adjust layout
    ax.set_title('Weekly Course Timetable', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('course_timetable.png', dpi=300, bbox_inches='tight')
    print("Timetable has been saved as 'course_timetable.png'")
    
    # Show the figure
    plt.show()

def main():
    # Find JSON files
    json_files = find_json_files()
    
    # Let user select a file
    selected_file = select_json_file(json_files)
    
    if selected_file:
        try:
            # Load the selected JSON file
            with open(selected_file, 'r', encoding='utf-8') as f:
                courses_data = json.load(f)
            
            # Draw the timetable
            draw_timetable(courses_data)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()