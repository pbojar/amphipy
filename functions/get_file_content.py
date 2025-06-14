from .constrain_to_pwd import constrain_to_pwd
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    pwd, f_path = constrain_to_pwd(working_directory, file_path, "read")
    if not pwd:
        return f_path
    if not f_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with f_path.open("r") as f:
            content = f.read(MAX_CHARS)
            if f.readline():
                content += f'\n[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
