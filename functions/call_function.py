from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python import run_python_file
from .write_file import write_file

from google.genai import types


func_dict = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}
work_dir = {"working_directory": "./calculator"}


def call_function(func_call_part, verbose=False):
    func_name = func_call_part.name
    args = work_dir | func_call_part.args
    call_msg = f" - Calling function: {func_name}"
    if verbose:
        call_msg += f"({args})"
    print(call_msg)
    if func_name not in func_dict.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": func_dict[func_name](**args)},
            )
        ],
    )
