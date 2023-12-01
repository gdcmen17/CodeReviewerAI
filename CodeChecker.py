import subprocess

class CodeChecker:
    def __init__(self, code):
        self.code = code
        self.error_output = ""

    def contains_syntax_error(self):
        # Save the code to a temporary file
        with open("temp.cpp", "w") as file:
            file.write(self.code)

        # Run the compiler and capture its output
        compile_command = "g++ -fsyntax-only temp.cpp 2> error.txt"
        result = subprocess.call(compile_command, shell=True)

        # Check the compilation result
        if result != 0:
            # Compilation failed, check the error output
            with open("error.txt", "r") as error_file:
                for line in error_file:
                    if "error" in line:
                        return True  # Found an error message

        return False  # No syntax errors found

    def analyze_code(self):
        # Simulate analyzing code and checking for syntax errors
        print("Analyzing code...")

        if not self.code:
            print("No code provided. Please input some code.")
            return

        try:
            if self.contains_syntax_error():
                # define what type of errors
                raise Exception("SyntaxError")
            else:
                print("No syntax errors found in the code.")

        except Exception as validator:
            if str(validator) == "SyntaxError":
                print("Syntax error found in the code.")
                try:
                    with open("error.txt", "r") as error_file:
                        for line in error_file:
                            print(line.strip())
                except FileNotFoundError:
                    print("Error reading from error.txt")