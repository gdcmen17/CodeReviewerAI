import tkinter as tk
from CodeChecker import CodeChecker
from tkinter import scrolledtext, filedialog

class CodeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assisted Software Testing Tool")
        self.root.geometry("1280x720")  # Set the initial dimensions as needed

        self.create_widgets()

    def create_widgets(self):
        # Frame for code input and result output
        self.input_output_frame = tk.Frame(self.root)
        self.input_output_frame.pack(expand=True, fill=tk.BOTH)

        # Frame for code input
        self.code_input_frame = tk.Frame(self.input_output_frame)
        self.code_input_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.code_input_label = tk.Label(self.code_input_frame, text="Enter the code here:")
        self.code_input_label.pack(anchor="w", padx=10, pady=10)

        self.code_input = scrolledtext.ScrolledText(self.code_input_frame, wrap=tk.WORD, width=50, height=25)
        self.code_input.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Frame for code output
        self.result_output_frame = tk.Frame(self.input_output_frame)
        self.result_output_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.code_output_label = tk.Label(self.result_output_frame, text="Code Result Output:")
        self.code_output_label.pack(anchor="w", padx=10, pady=10)

        self.result_text = scrolledtext.ScrolledText(self.result_output_frame, wrap=tk.WORD, width=50, height=25)
        self.result_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.analyze_button = tk.Button(self.button_frame, text="Analyze Code", command=self.analyze_code)
        self.analyze_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_file_button = tk.Button(self.button_frame, text="Load Code from File", command=self.load_code_from_file)
        self.load_file_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_file_button = tk.Button(self.button_frame, text="Save Code to File", command=self.save_code_to_file)
        self.save_file_button.pack(side=tk.LEFT, padx=5, pady=5)

    def analyze_code(self):
        code_to_check = self.code_input.get("1.0", tk.END)
        # Create CodeChecker instance and analyze the code
        code_checker = CodeChecker(code=code_to_check)
        code_checker.analyze_code()

        # Extract and format the desired parts of the analysis result
        analysis_result = code_checker.log_stream.getvalue()
        lines = analysis_result.strip().split('\n')

        # Filter lines based on the desired criteria
        filtered_lines = [
            line for line in lines
            if "Analyzing code" in line
            or "Syntax error" in line
            or "AI Suggestion" in line
            or "AI analysis completed" in line
            or "Analysis completed" in line
            or "No syntax errors found in the code" in line
        ]

        # Display the formatted analysis result in the result_text
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, '\n'.join(filtered_lines))


    # Opens a file from the computer or desired source, and displays the text in the interface
    def load_code_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code_from_file = file.read()
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, code_from_file)

    # Saves the code into a file
    def save_code_to_file(self):
        code_to_save = self.code_input.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(code_to_save)

# Main function, calls the interface to work
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCheckerApp(root)
    root.mainloop()
