## Welcome to the main file of this repository
# MainCode.py
from CodeChecker import CodeChecker # We import the class like this because if not it would have been treated like a module
from FileHandler import FileHandler
import logging
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script directory
os.chdir(script_dir)

logging.basicConfig(level=logging.INFO)
#code_to_check = str(input("Enter the code to analyze: "))

#checker = CodeChecker(code = code_to_check)
#checker.analyze_code()  

print("Now we are analyzing the file")
filename = "CodeToRead.txt"

# Read code from file using FileHandler
code_to_check = FileHandler.read_code_from_file(filename)

# Check if code is not None (i.e., file reading was successful)
if code_to_check is not None:
    # Create CodeChecker instance and analyze the code
    FileChecker = CodeChecker(code=code_to_check)
    FileChecker.analyze_code()
else:
    print("Error reading code from file. Please check the file.")

# You can also write the code back to a file if needed
# FileHandler.write_code_to_file("NewCodeFile.txt", code_to_check)
