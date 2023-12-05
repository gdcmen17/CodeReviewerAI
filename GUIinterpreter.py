import tkinter as tk
from tkinter import scrolledtext, filedialog
from CodeChecker import CodeChecker
from FileHandler import FileHandler

class CodeCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Checker App")

        self.create_widgets()

    def create_widgets(self):
        # Create a text area for code input
        self.code_input_label = tk.Label(self.root, text="Enter the code to analyze:")
        self.code_input_label.pack()

        self.code_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.code_input.pack()

        # Create a button to analyze code
        self.analyze_button = tk.Button(self.root, text="Analyze Code", command=self.analyze_code)
        self.analyze_button.pack()

        # Create a button to load code from a file
        self.load_file_button = tk.Button(self.root, text="Load Code from File", command=self.load_code_from_file)
        self.load_file_button.pack()

        # Create a button to save code to a file
        self.save_file_button = tk.Button(self.root, text="Save Code to File", command=self.save_code_to_file)
        self.save_file_button.pack()

        # Create a text area for displaying results
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.result_text.pack()

    def analyze_code(self):
        code_to_check = self.code_input.get("1.0", tk.END)  # Get code from the text area
        checker = CodeChecker(code=code_to_check)
        checker.analyze_code()

        # Display the results in the result_text area
        self.result_text.delete("1.0", tk.END)  # Clear previous results
        self.result_text.insert(tk.END, "Analysis Results:\n")
        self.result_text.insert(tk.END, checker.log.handlers[0].stream.getvalue())

    def load_code_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            code_from_file = FileHandler.read_code_from_file(file_path)
            self.code_input.delete("1.0", tk.END)  # Clear previous code
            self.code_input.insert(tk.END, code_from_file)

    def save_code_to_file(self):
        code_to_save = self.code_input.get("1.0", tk.END)  # Get code from the text area
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            FileHandler.write_code_to_file(file_path, code_to_save)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCheckerApp(root)
    root.mainloop()
