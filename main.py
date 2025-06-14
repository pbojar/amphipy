import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

def print_token_usage(usage_metadata):
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Chat with gemini-2.0-flash-001.")
    parser.add_argument("prompt", type=str, help="A prompt for gemini.")
    parser.add_argument("--verbose", help="Toggle for verbose output.", 
                        required=False, action="store_true")
    args = parser.parse_args()
    
    # Set-up initial query
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can 
    perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need 
    to specify the working directory in your function calls as it is automatically 
    injected for security reasons.
    """
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    # Function schema
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes," \
                    " constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the " \
                                "working directory. If not provided, lists files in the " \
                                "working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Outputs contents of specified file within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to output, relative to the " \
                                "working directory. Must be provided.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes Python (.py) file within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to run, relative to the working" \
                                " directory. Must be provided.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a file within the working directory. Cannot " \
                    "write to files outside the working directory. Will create a file " \
                    "if one does not exist.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write to, relative to the working" \
                                " directory. Must be provided.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write to the file. Must be provided.",
                ),
            },
        ),
    )
    # Available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    try:
        config = types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )
    except genai.errors.ServerError:
        print("Model is overloaded. Try again later!")
        sys.exit(1)
    
    # Print function calls
    for func_call in response.function_calls:
        print(f"Calling function: {func_call.name}({func_call.args})")
    # Print response
    print(response.text)
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print_token_usage(response.usage_metadata)
