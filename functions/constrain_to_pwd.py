from pathlib import Path


def constrain_to_pwd(working_directory, object_path, err_str="open"):
    pwd = Path(working_directory).absolute()
    obj_path = pwd.joinpath(object_path).resolve().absolute()
    if not str(obj_path).startswith(str(pwd)):
        err = f'Error: Cannot {err_str} "{object_path}" as it is outside the permitted '\
               'working directory'
        return False, err
    return pwd, obj_path
