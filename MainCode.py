## Welcome to the main file of this repository

from CodeChecker import CodeChecker # We import the class like this because if not it would have been treated like a module

code_to_check = str(input("Enter the code to analyze: "))

checker = CodeChecker(code_to_check)
checker.analyze_code()  # Corrected method name to analyze_code
