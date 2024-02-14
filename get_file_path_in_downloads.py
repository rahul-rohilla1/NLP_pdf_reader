import os

def get_file_path_in_downloads(file_name):
    # Determine the Downloads directory path
    if os.name == 'nt':  # Windows
        downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:  # macOS and Linux
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Construct the full path to the file within the Downloads directory
    file_path = os.path.join(downloads_path, file_name)
    
    return file_path

