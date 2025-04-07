import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("320x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.current_value = ""
        self.display_value = tk.StringVar()
        self.display_value.set("0")
        self.operation = None
        self.first_value = None
        self.calculated = False

        # Create the UI components
        self.create_display()
        self.create_buttons()

    def create_display(self):
        """Create the calculator display area"""
        display_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        display_frame.pack(fill=tk.X, padx=10)
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_value,
            font=("Arial", 24),
            bd=5,
            relief=tk.SUNKEN,
            justify=tk.RIGHT,
            state="readonly"
        )
        self.display.pack(fill=tk.X)

    def create_buttons(self):
        """Create the calculator button grid"""
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button layout configuration
        button_layout = [
            ("C", "#ff6347", self.clear_all),
            ("CE", "#ff6347", self.clear_entry),
            ("/", "#4682b4", lambda: self.set_operation("/")),
            ("*", "#4682b4", lambda: self.set_operation("*")),
            
            ("7", "#f8f8f8", lambda: self.add_digit("7")),
            ("8", "#f8f8f8", lambda: self.add_digit("8")),
            ("9", "#f8f8f8", lambda: self.add_digit("9")),
            ("-", "#4682b4", lambda: self.set_operation("-")),
            
            ("4", "#f8f8f8", lambda: self.add_digit("4")),
            ("5", "#f8f8f8", lambda: self.add_digit("5")),
            ("6", "#f8f8f8", lambda: self.add_digit("6")),
            ("+", "#4682b4", lambda: self.set_operation("+")),
            
            ("1", "#f8f8f8", lambda: self.add_digit("1")),
            ("2", "#f8f8f8", lambda: self.add_digit("2")),
            ("3", "#f8f8f8", lambda: self.add_digit("3")),
            ("=", "#ff8c00", self.calculate),
            
            ("0", "#f8f8f8", lambda: self.add_digit("0")),
            (".", "#f8f8f8", lambda: self.add_decimal()),
            ("+/-", "#f8f8f8", self.toggle_sign),
            ("", "#f8f8f8", None),  # Empty button for layout
        ]

        # Create the button grid
        row, col = 0, 0
        for (text, bg_color, command) in button_layout:
            if text:  # Skip empty buttons
                # Create a special layout for the "=" button
                if text == "=":
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        bg=bg_color,
                        fg="white",
                        font=("Arial", 16),
                        relief=tk.RAISED,
                        bd=3,
                        command=command
                    )
                    btn.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=2, pady=2)
                else:
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        bg=bg_color,
                        fg="black" if bg_color != "#4682b4" and bg_color != "#ff6347" else "white",
                        font=("Arial", 16),
                        relief=tk.RAISED,
                        bd=3,
                        command=command
                    )
                    btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Configure grid weights to make buttons expand proportionally
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

    def add_digit(self, digit):
        """Add a digit to the current value"""
        if self.calculated:
            self.current_value = ""
            self.calculated = False
            
        self.current_value += digit
        self.update_display()

    def add_decimal(self):
        """Add a decimal point if not already present"""
        if self.calculated:
            self.current_value = "0"
            self.calculated = False
            
        if "." not in self.current_value:
            self.current_value = self.current_value + "." if self.current_value else "0."
        self.update_display()

    def clear_all(self):
        """Clear all values and operations"""
        self.current_value = ""
        self.first_value = None
        self.operation = None
        self.calculated = False
        self.display_value.set("0")

    def clear_entry(self):
        """Clear the current entry"""
        self.current_value = ""
        self.display_value.set("0")

    def toggle_sign(self):
        """Toggle the sign of the current value"""
        if not self.current_value:
            return
            
        if self.current_value.startswith("-"):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = "-" + self.current_value
        self.update_display()

    def set_operation(self, op):
        """Set the operation and store the first value"""
        if self.current_value:
            if self.first_value is not None:
                # If we already have a first value, calculate the result first
                self.calculate()
                
            self.first_value = float(self.current_value)
            self.operation = op
            self.current_value = ""
        elif self.first_value is not None:
            # Allow changing the operation if first value is already set
            self.operation = op

    def calculate(self):
        """Perform the calculation based on the current operation"""
        if not self.operation or not self.first_value:
            return
            
        if not self.current_value:
            self.current_value = str(self.first_value)
            return
            
        try:
            second_value = float(self.current_value)
            
            if self.operation == "+":
                result = self.first_value + second_value
            elif self.operation == "-":
                result = self.first_value - second_value
            elif self.operation == "*":
                result = self.first_value * second_value
            elif self.operation == "/":
                if second_value == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    self.clear_all()
                    return
                result = self.first_value / second_value
                
            # Format the result to avoid unnecessary decimal places
            if result == int(result):
                result = int(result)
                
            self.current_value = str(result)
            self.first_value = None
            self.operation = None
            self.calculated = True
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.clear_all()

    def update_display(self):
        """Update the display with the current value"""
        if not self.current_value:
            self.display_value.set("0")
        else:
            self.display_value.set(self.current_value)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
