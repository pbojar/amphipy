from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

tests = {
    "get_files_info":
    (
        get_files_info, 
        [
            ("calculator", "."),
            ("calculator", "pkg"),
            ("calculator", "/bin"),
            ("calculator", "../")
        ]
    ),
    "get_file_content" :
    (
        get_file_content,
        [
            ("calculator", "main.py"),
            ("calculator", "pkg/calculator.py"),
            ("calculator", "/bin/cat"),
        ]
    ),
    "write_file":
    (
        write_file,
        [
            ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
            ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
            ("calculator", "/tmp/temp.txt", "this should not be allowed"),
        ]
    ),
    "run_python_file":
    (
        run_python_file,
        [
            ("calculator", "main.py"),
            ("calculator", "tests.py"),
            ("calculator", "../main.py"),
            ("calculator", "nonexistent.py")    
        ]
    )
}

if __name__ == '__main__':

    func, args_list = tests["write_file"]
    for args in args_list:
        print(func(*args))
        print()
