import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    
    try:
        abspath_to_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath_to_working_directory, file_path))
        valid_target_file = os.path.commonpath([abspath_to_working_directory, target_file]) == abspath_to_working_directory

        if not valid_target_file:
            return f"    Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(target_file):
            return f"    Error: \"{file_path}\" does not exist or is not a regular file"
        
        if not target_file.endswith(".py"):
            return f"    Error: \"{file_path}\" is not a Python file"
        
        command = ["python", target_file]

        if args != None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        else:
            if completed_process.stdout:
                output.append(f"STDOUT:\n {completed_process.stdout}")
            if completed_process.stderr:
                output.append(f"STDERR:\n {completed_process.stderr}")

        return "\n".join(output)
    
    except Exception as e:
        return f"    Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python program specified as the file path with the arguments given (none if not specified by default)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content from, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to be passed to the file program (None by default)",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="One of the arguments to be passed to the file program"
                )
            )
        },
    ),
)
