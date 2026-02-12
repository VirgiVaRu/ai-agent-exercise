import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    try:
        abspath_to_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_to_working_directory, file_path))
        valid_target_file = os.path.commonpath([abspath_to_working_directory, target_file]) == abspath_to_working_directory

        if not valid_target_file:
            return f"    Error: cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(target_file):
            return f"    Error: File not found or is not a regular file: \"{file_path}\""
        
        file = open(target_file)
        contents = file.read(MAX_CHARS)
        if file.read(1):
            contents += f"[...File \"{file_path}\" truncated at {MAX_CHARS}]"

        return contents
    
    except Exception as e:
        return f"    Error: {e}"