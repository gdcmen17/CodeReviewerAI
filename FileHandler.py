# FileHandler.py

import os

class FileHandler:
    @staticmethod
    # Function that read codes from file
    def read_code_from_file(filename):
        try:
            with open(filename, "r") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading code from file {filename}: {e}")
            return None

    # Function that writes the code into a file
    @staticmethod
    def write_code_to_file(filename, code):
        try:
            with open(filename, "w") as file:
                file.write(code)
            print(f"Code written to file {filename}.")
        except Exception as e:
            print(f"Error writing code to file {filename}: {e}")