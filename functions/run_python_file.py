import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory with optional command-line arguments and returns the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}



def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
                
        # Will be True or False
        valid_target_path = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
                
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                
        # Check if the target path exists and is an actual directory
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
                
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
            
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )


        output_str = ""
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode}\n"
            
        if result.stderr == "" and result.stdout == "":
            output_str += f"No output produced\n"
        else:
            if result.stdout != "":
                output_str += f"STDOUT: {result.stdout}\n"
                    
            if result.stderr != "":
                output_str += f"STDERR: {result.stderr}\n"

                
                
        return output_str
        
    except Exception as e:
                return f"Error: executing Python file: {e}"