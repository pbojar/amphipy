from .constrain_to_pwd import constrain_to_pwd


def write_file(working_directory, file_path, content):
    pwd, f_path = constrain_to_pwd(working_directory, file_path, "write to")
    if not pwd:
        return f_path
    if not f_path.exists():
        try:
            f_path.touch()
        except Exception as e:
            return f'Error creating "{file_path}"'
    try:
        with f_path.open("w") as f:
            f.write(content)
    except Exception as e:
        return f'Error writing to "{file_path}"'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
