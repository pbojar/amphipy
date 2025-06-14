import subprocess
from .constrain_to_pwd import constrain_to_pwd


def run_python_file(working_directory, file_path):
    pwd, f_path = constrain_to_pwd(working_directory, file_path, "execute")
    if not pwd:
        return f_path
    if not f_path.exists():
        return f'Error: File "{file_path}" not found'
    if f_path.suffix != ".py":
        return f'Error: File "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python3", str(f_path)], timeout=30, cwd=pwd, \
                                check=True, text=True, capture_output=True)
    except Exception as e:
        return f'Error: executing "{file_path}": {e}'
    if not result.stdout and not result.stderr:
        return "No output produced"
    output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n"
    if result.returncode != 0:
        output += f"Process exited with code {result.returncode}\n"
    return output
