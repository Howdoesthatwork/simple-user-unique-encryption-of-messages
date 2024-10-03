import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Define file paths
mappings_file_path = 'textas.txt'
translations_file_path = 'translations.txt'

def save_mappings_to_file(ascii_to_letter, file_path):
    """Saves ASCII mappings to a specified text file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for ascii_repr, letter in ascii_to_letter.items():
            f.write(f"{ascii_repr} {letter}\n")

def load_mappings_from_file(file_path):
    """Loads ASCII mappings from a specified text file."""
    ascii_to_letter = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.rsplit(' ', 1)  # Split on the last space
                if len(parts) == 2:
                    ascii_repr = parts[0].strip()
                    letter = parts[1].strip()
                    ascii_to_letter[ascii_repr] = letter
    return ascii_to_letter

def translate_letters_to_ascii(text, letter_to_ascii):
    """Translates plain text letters into their ASCII representations."""
    text = text.lower()  # Convert input to lowercase
    translated_ascii = ""
    for char in text:
        if char in letter_to_ascii:
            translated_ascii += letter_to_ascii[char] + "\n\n"
        else:
            translated_ascii += "Unknown character\n\n"

    return translated_ascii.strip()

def translate_ascii_to_letters(text, ascii_to_letter):
    """Translates ASCII representations back to their letters."""
    translated_letters = ""
    ascii_lines = text.split()  # Split by spaces
    for ascii_line in ascii_lines:
        if ascii_line in ascii_to_letter:
            translated_letters += ascii_to_letter[ascii_line]
        else:
            translated_letters += "Unknown ASCII "

    return translated_letters.strip()

def perform_translation():
    """Handles the translation based on user input."""
    action = action_var.get()
    input_text = input_text_box.get("1.0", tk.END).strip()

    if action == "translate":
        direction = direction_var.get()
        if direction == "letters_to_ascii":
            result = translate_letters_to_ascii(input_text, {v: k for k, v in ascii_to_letter.items()})
            output_text_box.delete("1.0", tk.END)
            output_text_box.insert(tk.END, result)

            # Save translation to file
            with open(translations_file_path, 'a', encoding='utf-8') as f:
                f.write(f"Input: {input_text}\nOutput: {result}\n\n")

        elif direction == "ascii_to_letters":
            result = translate_ascii_to_letters(input_text, ascii_to_letter)
            output_text_box.delete("1.0", tk.END)
            output_text_box.insert(tk.END, result)

            # Save translation to file
            with open(translations_file_path, 'a', encoding='utf-8') as f:
                f.write(f"Input: {input_text}\nOutput: {result}\n\n")

def add_mappings():
    """Adds new ASCII mappings entered by the user."""
    mapping_input = mapping_text_box.get("1.0", tk.END).strip()
    if not mapping_input:
        messagebox.showwarning("Warning", "Please enter a mapping in the format 'ASCII representation letter'.")
        return

    try:
        ascii_repr, letter = mapping_input.rsplit(' ', 1)  # Split on the last space
        ascii_repr = ascii_repr.strip()
        letter = letter.strip()

        # Add to the current mappings
        ascii_to_letter[ascii_repr] = letter
        save_mappings_to_file(ascii_to_letter, mappings_file_path)

        # Clear the mapping input box and notify the user
        mapping_text_box.delete("1.0", tk.END)
        messagebox.showinfo("Success", f"Mapping added: '{ascii_repr}' -> '{letter}'")
    except ValueError:
        messagebox.showerror("Error", "Invalid input format. Please use 'ASCII representation letter'.")

def delete_mappings():
    """Deletes the last mapping from the mappings file."""
    if not os.path.exists(mappings_file_path):
        messagebox.showwarning("Warning", "No mapping file found to delete from.")
        return

    with open(mappings_file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            messagebox.showwarning("Warning", "No mappings to delete.")
            return
        lines.pop()  # Remove the last line (last mapping)
        f.seek(0)
        f.truncate()  # Clear the file
        f.writelines(lines)  # Rewrite the remaining lines

    load_mappings()  # Reload mappings
    messagebox.showinfo("Success", "Last mapping deleted.")

def load_mappings():
    """Reloads mappings from the file."""
    global ascii_to_letter
    ascii_to_letter = load_mappings_from_file(mappings_file_path)

def show_description():
    """Displays a brief description of the program."""
    messagebox.showinfo("Description", "This program translates letters to ASCII representations and vice versa.\n"
                                         "You can also add your own mappings.")

# Initialize the main application window
app = tk.Tk()
app.title("ASCII Translator")
app.geometry("600x600")

# Show the description when the program starts
show_description()

# Load existing mappings from file
ascii_to_letter = load_mappings_from_file(mappings_file_path)

# Create GUI elements
action_var = tk.StringVar(value="translate")
direction_var = tk.StringVar(value="letters_to_ascii")

# Action selection
action_frame = tk.Frame(app)
action_frame.pack(pady=10)
tk.Label(action_frame, text="Select Action:").pack(side=tk.LEFT)
tk.Radiobutton(action_frame, text="Add Mappings", variable=action_var, value="add_mappings").pack(side=tk.LEFT)
tk.Radiobutton(action_frame, text="Translate", variable=action_var, value="translate").pack(side=tk.LEFT)

# Direction selection (for translation)
direction_frame = tk.Frame(app)
direction_frame.pack(pady=10)
tk.Label(direction_frame, text="Direction:").pack(side=tk.LEFT)
tk.Radiobutton(direction_frame, text="Letters to ASCII", variable=direction_var, value="letters_to_ascii").pack(side=tk.LEFT)
tk.Radiobutton(direction_frame, text="ASCII to Letters", variable=direction_var, value="ascii_to_letters").pack(side=tk.LEFT)

# Mapping input box for adding mappings
tk.Label(app, text="Add Mapping (ASCII representation letter):").pack(pady=5)
mapping_text_box = scrolledtext.ScrolledText(app, width=70, height=3)
mapping_text_box.pack(pady=5)

# Add Mapping button
add_mapping_button = tk.Button(app, text="Add Mapping", command=add_mappings)
add_mapping_button.pack(pady=10)

# Delete Mapping button
delete_mapping_button = tk.Button(app, text="Delete Last Mapping", command=delete_mappings)
delete_mapping_button.pack(pady=10)

# Input text box
tk.Label(app, text="Input:").pack(pady=5)
input_text_box = scrolledtext.ScrolledText(app, width=70, height=5)
input_text_box.pack(pady=5)

# Translate button
translate_button = tk.Button(app, text="Translate", command=perform_translation)
translate_button.pack(pady=10)

# Output text box
tk.Label(app, text="Output:").pack(pady=5)
output_text_box = scrolledtext.ScrolledText(app, width=70, height=5)
output_text_box.pack(pady=5)

# Run the application
app.mainloop()
