import os
from config import MAX_CHARS


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}



def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path  = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_abs_file_path  = os.path.commonpath([working_dir_abs, abs_file_path ]) == working_dir_abs
        
        if not valid_abs_file_path :
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path ):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
    
        # Reading the file
        with open(abs_file_path  , "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"