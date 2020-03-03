import subprocess
import sys

from os.path import abspath, join, dirname


if __name__ == "__main__":
    command = sys.argv[1:]
    if getattr(sys, "frozen", False):
        project_path = dirname(sys.executable)
    elif __file__:
        project_path = dirname(__file__)
    venv_python_path = join(project_path, ".venv", "Scripts")
    main_python_path = join(project_path, "main.py")
    if command:
        complete_command = ["python.exe", main_python_path] + command
    else:
        complete_command = ["python.exe", main_python_path, "-h"]
    subprocess.call(complete_command, cwd=venv_python_path, shell=True)
