#!/usr/bin/env python3
"""
SCHEDULE MAKER - PYTHON BACKEND
This Python script serves as the backend for the Weekly Schedule Maker web application.

Features:
1. HTTP server that communicates with the HTML frontend
2. Scans user's Downloads folder for JSON files
3. Loads and processes class schedule JSON data
4. Rounds class times to 30-minute intervals (9:00-20:00 range)
5. Converts time formats and validates schedule data
6. Sends processed class data to frontend via HTTP API

API Endpoints:
- GET /get_json_files: Returns list of JSON files in Downloads folder
- POST /load_json: Loads and processes a specific JSON file
- CORS enabled for local frontend communication

JSON Format Expected:
[
  [
    "class_code",
    "class_name", 
    "teacher_name",
    ["DAY : HH:MM - HH:MM", ...],
    "classroom",
    "capacity"
  ],
  ...
]

Time Processing:
- Rounds down start times to nearest 30-minute interval
- Rounds up end times to nearest 30-minute interval
- Ensures times fall within 9:00-20:00 range
"""

import json
import os
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser
from datetime import datetime

class ScheduleHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/get_json_files':
            self.get_json_files()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/load_json':
            self.load_json_file()
        else:
            self.send_error(404, "Endpoint not found")
    
    def get_json_files(self):
        """Return list of JSON files in Downloads folder"""
        try:
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            json_files = []
            
            if os.path.exists(downloads_path):
                for file in os.listdir(downloads_path):
                    if file.lower().endswith('.json'):
                        json_files.append(file)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(json_files)
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error getting JSON files: {str(e)}")
    
    def load_json_file(self):
        """Load and process a specific JSON file"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            filename = request_data.get('filename')
            if not filename:
                self.send_error(400, "Filename not provided")
                return
            
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            file_path = os.path.join(downloads_path, filename)
            
            if not os.path.exists(file_path):
                self.send_error(404, f"File {filename} not found")
                return
            
            # Load and process JSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_classes = json.load(f)
            
            processed_classes = self.process_classes(raw_classes)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(processed_classes, ensure_ascii=False, indent=2)
            self.wfile.write(response.encode('utf-8'))
            
            print(f"Successfully loaded and processed {filename}")
            print(f"Found {len(processed_classes)} classes")
            
        except json.JSONDecodeError as e:
            self.send_error(400, f"Invalid JSON format: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Error loading JSON file: {str(e)}")
    
    def process_classes(self, raw_classes):
        """Process raw class data and round times to 30-minute intervals"""
        processed = []
        
        for class_data in raw_classes:
            if len(class_data) < 6:
                continue  # Skip malformed entries
            
            class_code, class_name, teacher, time_slots, classroom, capacity = class_data
            
            # Process time slots
            processed_slots = []
            for time_slot in time_slots:
                processed_slot = self.process_time_slot(time_slot)
                if processed_slot:
                    processed_slots.append(processed_slot)
            
            if processed_slots:  # Only add classes with valid time slots
                processed.append({
                    'code': class_code,
                    'name': class_name,
                    'teacher': teacher,
                    'timeSlots': processed_slots,
                    'classroom': classroom,
                    'capacity': capacity
                })
        
        return processed
    
    def process_time_slot(self, time_slot):
        """Process a single time slot and round to 30-minute intervals"""
        try:
            # Parse format: "DAY : HH:MM - HH:MM"
            parts = time_slot.split(' : ')
            if len(parts) != 2:
                return None
            
            day = parts[0].strip().upper()
            time_range = parts[1].strip()
            
            # Parse time range
            time_parts = time_range.split(' - ')
            if len(time_parts) != 2:
                return None
            
            start_time = time_parts[0].strip()
            end_time = time_parts[1].strip()
            
            # Round times
            rounded_start = self.round_time_down(start_time)
            rounded_end = self.round_time_up(end_time)
            
            # Validate times are within schedule range (9:00-20:00)
            if not self.is_valid_time_range(rounded_start, rounded_end):
                return None
            
            return f"{day} : {rounded_start} - {rounded_end}"
            
        except Exception as e:
            print(f"Error processing time slot '{time_slot}': {str(e)}")
            return None
    
    def round_time_down(self, time_str):
        """Round time down to nearest 30-minute interval"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            
            # Round minutes down to nearest 30
            if minutes < 30:
                minutes = 0
            else:
                minutes = 30
            
            # Ensure within bounds
            if hours < 9:
                hours, minutes = 9, 0
            elif hours >= 20:
                hours, minutes = 19, 30
            
            return f"{hours:02d}:{minutes:02d}"
            
        except Exception:
            return "09:00"  # Default fallback
    
    def round_time_up(self, time_str):
        """Round time up to nearest 30-minute interval"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            
            # Round minutes up to nearest 30
            if minutes == 0:
                pass  # Already on interval
            elif minutes <= 30:
                minutes = 30
            else:
                minutes = 0
                hours += 1
            
            # Ensure within bounds
            if hours < 9:
                hours, minutes = 9, 30
            elif hours > 20 or (hours == 20 and minutes > 0):
                hours, minutes = 20, 0
            
            return f"{hours:02d}:{minutes:02d}"
            
        except Exception:
            return "09:30"  # Default fallback
    
    def is_valid_time_range(self, start_time, end_time):
        """Check if time range is valid (within 9:00-20:00)"""
        try:
            start_hours, start_minutes = map(int, start_time.split(':'))
            end_hours, end_minutes = map(int, end_time.split(':'))
            
            start_total = start_hours * 60 + start_minutes
            end_total = end_hours * 60 + end_minutes
            
            # Check bounds (9:00 to 20:00)
            min_time = 9 * 60  # 9:00 in minutes
            max_time = 20 * 60  # 20:00 in minutes
            
            return (start_total >= min_time and 
                    end_total <= max_time and 
                    start_total < end_total)
            
        except Exception:
            return False
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def start_server():
    """Start the HTTP server"""
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ScheduleHandler)
    
    print("=" * 60)
    print("📅 SCHEDULE MAKER BACKEND SERVER")
    print("=" * 60)
    print(f"🚀 Server running on http://localhost:8000")
    print(f"📁 Monitoring Downloads folder: {os.path.join(os.path.expanduser('~'), 'Downloads')}")
    print("🌐 CORS enabled for frontend communication")
    print("=" * 60)
    print("Available endpoints:")
    print("  GET  /get_json_files  - List JSON files in Downloads")
    print("  POST /load_json       - Load and process JSON file")
    print("=" * 60)
    print("💡 Make sure your HTML file is open in a browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.server_close()

def test_time_processing():
    """Test function to verify time processing logic"""
    handler = ScheduleHandler()
    
    test_cases = [
        "MON : 09:20 - 11:20",  # Should become "MON : 09:00 - 11:30"
        "TUE : 14:45 - 16:15",  # Should become "TUE : 14:30 - 16:30"
        "WED : 08:30 - 10:00",  # Should become "WED : 09:00 - 10:00"
        "THU : 18:30 - 21:00",  # Should become "THU : 18:30 - 20:00"
        "FRI : 13:00 - 14:30",  # Should stay "FRI : 13:00 - 14:30"
    ]
    
    print("\n🧪 Testing time processing:")
    print("-" * 40)
    for test_case in test_cases:
        result = handler.process_time_slot(test_case)
        print(f"Input:  {test_case}")
        print(f"Output: {result}")
        print("-" * 40)

def check_downloads_folder():
    """Check if Downloads folder exists and is accessible"""
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    if not os.path.exists(downloads_path):
        print(f"⚠️  Warning: Downloads folder not found at {downloads_path}")
        return False
    
    try:
        files = os.listdir(downloads_path)
        json_files = [f for f in files if f.lower().endswith('.json')]
        print(f"✅ Downloads folder accessible: {len(json_files)} JSON files found")
        return True
    except PermissionError:
        print(f"❌ Error: Permission denied accessing {downloads_path}")
        return False

if __name__ == "__main__":
    print("🔍 Checking system setup...")
    check_downloads_folder()
    
    # Uncomment the line below to test time processing logic
    # test_time_processing()
    
    index_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

    if os.path.exists(index_file):
        os.startfile(index_file)
    
    print("\n🚀 Starting schedule maker backend server...")
    start_server()