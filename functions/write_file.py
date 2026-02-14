import os
from google.genai import types

def write_file(working_directory, file_path, contents):
    try:
        abspath_to_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_to_working_directory, file_path))
        valid_target_file = os.path.commonpath([abspath_to_working_directory, target_file]) == abspath_to_working_directory

        if not valid_target_file:
            return f"    Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        
        if os.path.isdir(target_file):
            return f"    Error: Cannot write to \"{file_path}\" as it is a directory"
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as file:
            file.write(contents)
        return f"Successfully wrote to \"{file_path}\" ({len(contents)} characters written)"

    except Exception as e:
        return f"    Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents to the specified file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content from, relative to the working directory",
            ),
            "contents":types.Schema(
                type=types.Type.STRING,
                description="Text to be written in the file specified by the file path"
            )
        },
    ),
)
        