# CodeChecker.py

import subprocess
import os
import logging
from io import StringIO  # Import StringIO for capturing logs
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Configure the root logger with a basic configuration
logging.basicConfig(level=logging.INFO)

# Disable transformers library logging for this module
logging.getLogger("transformers").setLevel(logging.ERROR)

class CodeChecker:
    # Constructor, in which we will call all the external modules (https://github.com/microsoft/CodeBERT/tree/master/CodeReviewer) and initialize functions
    def __init__(self, code="", temp_filename="temp.cpp"):
        self.code = code
        self.temp_filename = temp_filename
        self.error_output = []

        # Use StringIO to capture logs
        self.log_stream = StringIO()
        self.log = logging.getLogger("CodeChecker")
        self.log.addHandler(logging.StreamHandler(self.log_stream))

        self.model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/codereviewer")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codereviewer")

    # Function that is called to chceck if there is any syntax errors, returns true if so
    def contains_syntax_error(self):
        try:
            with open(self.temp_filename, "w") as file:
                file.write(self.code)

            # Check if there is any syntax errors
            compile_command = f"g++ -fsyntax-only {self.temp_filename} 2> error.txt"
            result = subprocess.call(compile_command, shell=True)

            # If there is syntax errors, gets into the If
            if result != 0:
                with open("error.txt", "r") as error_file:
                    errors = [line.strip() for line in error_file if "error" in line]
                    self.error_output = errors  # Store all syntax errors in a list
                    return bool(errors)  # Return True if there are any syntax errors

        except Exception as e:
            self.log.error(f"Error in contains_syntax_error: {e}")

        finally:
            self.cleanup()

        return False  # Return False if no syntax errors were found

    # Function that gets called principally by the interpreter, analyzes the code for syntax errors and outputs a message in consequence
    def analyze_code(self, analyze_with_ai=True):
        try:
            self.log.info("Analyzing code...")

            if not self.code:
                self.log.warning("No code provided. Please input some code.")
                return

            # If it contains errors it gets called
            if self.contains_syntax_error():
                for error in self.error_output:
                    self.log.error(f"Syntax error: {error}")

                raise SyntaxError("Syntax errors found in the code.")

            self.log.info("No syntax errors found in the code.")

            # Calls AI to analyze the code
            if analyze_with_ai:
                self.analyze_with_ai()

        except SyntaxError as se:
            self.log.error(str(se))
            
            # Whenever it receives a Syntax Error, also call the AI
            if analyze_with_ai:
                self.analyze_with_ai()

        # Error when alayzing code
        except Exception as e:
            self.log.error(f"Error in analyze_code: {e}")

        finally:
            self.cleanup()

    # AI gives suggestion aobut how the code could be fixed
    def analyze_with_ai(self):
        try:
            if self.error_output:
                self.log.info("Performing AI analysis for each syntax error...")

                # For every error it gives you a complete analysis
                for error in self.error_output:
                    error_line, error_position = self.get_error_position(error)

                    inputs = self.tokenizer(self.code, return_tensors="pt")
                    outputs = self.model.generate(**inputs)
                    prediction = self.tokenizer.decode(outputs[0])

                    self.log.info("AI analysis completed.")

                    # If the suggestion is to remove the file, it gives a more friendly suggestion
                    if "Remove this file." in prediction:
                        # Modify the suggestion to be more specific or helpful
                        suggestion = "Review and fix the code based on the reported syntax error."
                        prediction = "Review and fix the code based on the reported syntax error."
                        self.log.info(f"AI Suggestion for error at line {error_line}: {suggestion}")

        except Exception as e:
            self.log.error(f"Error in analyze_with_ai: {e}")

    # Function that gets the error line and position
    def get_error_position(self, error):
        try:
            if error:
                error_line = int(error.split(":")[1])
                error_position = int(error.split(":")[2].split(" ")[0])
                return error_line, error_position
            else:
                return -1, -1
        except Exception as e:
            self.log.warning(f"Error getting error position: {e}")
            return -1, -1

    # Cleans up the temporary files that are created to work with the errors and the code inserted
    def cleanup(self):
        try:
            if os.path.exists(self.temp_filename):
                self.log.info(f"Removing {self.temp_filename}")
                os.remove(self.temp_filename)
            else:
                self.log.warning(f"{self.temp_filename} not found during cleanup")

            if os.path.exists("error.txt"):
                self.log.info("Removing error.txt")
                os.remove("error.txt")
            else:
                self.log.warning("error.txt not found during cleanup")
        except Exception as e:
            self.log.warning(f"Error during cleanup: {e}")
