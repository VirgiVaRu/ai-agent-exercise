import os

def get_files_info(working_directory, directory=""):
    try:

        if directory == ".":
            directory_name = "current"
        else:
            directory_name = f"\'{directory}\'"
        print(f"Result for {directory_name} directory:")

        abspath_to_working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abspath_to_working_directory, directory))
        valid_target_directory = os.path.commonpath([abspath_to_working_directory, target_directory]) == abspath_to_working_directory

        if not valid_target_directory:
            return f"    Error: cannot list \"{directory}\" as it is outside the permitted working directory"
        
        if not os.path.isdir(target_directory):
            return f"    Error: \"{directory}\" is not a directory"
        

        
        contents = []
        for file in os.listdir(target_directory):
            name = file
            abspath_to_file = os.path.normpath(os.path.join(target_directory, file))
            size = os.path.getsize(abspath_to_file)
            is_dir = os.path.isdir(abspath_to_file)
            contents.append(f"  - {name}: file_size={size}, is_dir={is_dir}")

        return "\n".join(contents)
    
    except Exception as e:
        return f"    Error: {e}"
