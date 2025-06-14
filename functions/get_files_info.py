from .constrain_to_pwd import constrain_to_pwd


def get_files_info(working_directory, directory=None):
    pwd, dir_path = constrain_to_pwd(working_directory, directory, "list")
    print(pwd, dir_path)
    if not pwd:
        return dir_path
    if not dir_path.is_dir():
        return f'Error: "{directory}" is not a directory'
    try:
        contents = ""
        for p in dir_path.iterdir():
            contents += \
                f"- {p.name}: file_size={p.stat().st_size} bytes, is_dir={p.is_dir()}\n"
        return contents
    except Exception as e:
        return f'Error getting info in "{directory}": {e}'
