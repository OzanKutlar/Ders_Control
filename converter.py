import re
import pyperclip

def process_bookmark_js(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    clean_lines = []
    for line in lines:
        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        clean_lines.append(line)
    
    cleaned_text = ''.join(clean_lines)
    
    cleaned_text = re.sub(r'[\s]\n', '', cleaned_text)
    cleaned_text = re.sub(r'[\n]', '', cleaned_text)
    
    bookmarklet = f"javascript:(() => {{ {cleaned_text} }})();"
    
    pyperclip.copy(bookmarklet)
    print("Bookmarklet has been copied to clipboard!")


process_bookmark_js('browserInject.js')
