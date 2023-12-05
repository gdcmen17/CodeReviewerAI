# CodeChecker.py

import subprocess
import os
import logging
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Disable transformers library logging for this module
logging.getLogger("transformers").setLevel(logging.ERROR)

class CodeChecker:
    def __init__(self, code="", temp_filename="temp.cpp"):
        self.code = code
        self.temp_filename = temp_filename
        self.error_output = ""
        self.log = logging.getLogger("CodeChecker")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/codereviewer")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codereviewer")
    
    def contains_syntax_error(self):
        try:
            with open(self.temp_filename, "w") as file:
                file.write(self.code)

            compile_command = f"g++ -fsyntax-only {self.temp_filename} 2> error.txt"
            result = subprocess.call(compile_command, shell=True)

            if result != 0:
                with open("error.txt", "r") as error_file:
                    errors = [line.strip() for line in error_file if "error" in line]
                    self.error_output = "\n".join(errors)
                    return True

        except Exception as e:
            self.log.error(f"Error in contains_syntax_error: {e}")

        finally:
            self.cleanup()

        return False

    def analyze_code(self, analyze_with_ai=True):
        try:
            self.log.info("Analyzing code...")

            if not self.code:
                self.log.warning("No code provided. Please input some code.")
                return

            if self.contains_syntax_error():
                raise SyntaxError("Syntax error found in the code.")

            self.log.info("No syntax errors found in the code.")



        except SyntaxError as se:
            self.log.error(str(se))
            self.log.error(self.error_output)
            self.log.error(f"The error was in line {self.get_error_line()} and in the position {self.get_error_position()}")
            
            # Whenever it receives a Syntax Error, also call the AI
            if analyze_with_ai:
                self.analyze_with_ai()


        except Exception as e:
            self.log.error(f"Error in analyze_code: {e}")

        finally:
            self.cleanup()

    def analyze_with_ai(self):
        try:
            if self.error_output:
                error_line, error_position = self.get_error_position()
                self.log.info(f"AI analysis is skipped due to syntax errors in line {error_line} at position {error_position}.")
                return

            self.log.info("Performing AI analysis...")

            inputs = self.tokenizer(self.code, return_tensors="pt")
            outputs = self.model.generate(**inputs)
            prediction = self.tokenizer.decode(outputs[0])

            self.log.info("AI analysis completed.")
            self.log.info("AI Prediction:")
            self.log.info(prediction)
            
            if "Remove this file." in prediction:
                # Modify the suggestion to be more specific or helpful
                suggestion = "Review and fix the code based on the reported syntax error."
                prediction = "Review and fix the code based on the reported syntax error."
                self.log.info(f"Suggestion: {suggestion}")

            error_line, error_position = self.get_error_position()
            self.log.info(f"AI analysis is skipped due to syntax errors in line {error_line} at position {error_position}.")
            self.log.info("Fixed Code:")
            fixed_code = self.get_fixed_code(prediction)
            self.log.info(fixed_code)

        except Exception as e:
            self.log.error(f"Error in analyze_with_ai: {e}")

    def get_error_line(self):
        try:
            return int(self.error_output.split(":")[1])
        except Exception as e:
            self.log.warning(f"Error getting error line: {e}")
            return -1

    def get_error_position(self):
        try:
            return int(self.error_output.split(":")[2].split(" ")[0])
        except Exception as e:
            self.log.warning(f"Error getting error position: {e}")
            return -1

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