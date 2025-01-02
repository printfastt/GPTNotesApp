import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser, font
import json
import os
from tkinter import ttk
import pyperclip

# Import the ask_chatgpt function from ai.py
from ai import ask_chatgpt

# File to store the notes in the current working directory
SAVE_FILE = os.path.join(os.getcwd(), "notes.json")

# Create the main window with a professional title and icon
window = tk.Tk()
window.title("CS3530 Notes")
window.geometry("800x600")  # Set a default window size
window.minsize(600, 400)  # Set minimum window size

# Apply a style theme using ttk
style = ttk.Style()
style.theme_use('clam')  # Base theme

# Define fonts
default_font = font.Font(family='Arial', size=12)
treeview_font = font.Font(family='Helvetica', size=10)

# Customize the style to use shades of gray and modern scrollbars
style.configure('Gray.TFrame', background='#2E2E2E')
style.configure('Gray.TButton', background='#3C3C3C', foreground='#FFFFFF', borderwidth=0, relief='flat')
style.map('Gray.TButton',
          background=[('active', '#4D4D4D')],
          foreground=[('disabled', '#A9A9A9')])
style.configure('Gray.TLabel', background='#2E2E2E', foreground='#FFFFFF')
style.configure('Gray.Treeview', font=treeview_font, background='#3C3C3C', foreground='#FFFFFF',
                fieldbackground='#3C3C3C', bordercolor='#2E2E2E', borderwidth=0)
style.map('Gray.Treeview',
          background=[('selected', '#5A5A5A')])
style.configure('Gray.TCombobox', fieldbackground='#3C3C3C', background='#3C3C3C', foreground='#FFFFFF',
                bordercolor='#2E2E2E', darkcolor='#2E2E2E', lightcolor='#2E2E2E', borderwidth=0)
style.map('Gray.TCombobox',
          fieldbackground=[('readonly', '#3C3C3C')])
style.configure('Vertical.Gray.TScrollbar', gripcount=0,
                background='#2E2E2E', darkcolor='#2E2E2E', lightcolor='#2E2E2E',
                troughcolor='#3C3C3C', bordercolor='#2E2E2E', arrowcolor='#FFFFFF')
style.layout('Vertical.Gray.TScrollbar',
             [('Vertical.Scrollbar.trough',
               {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])
# Define a custom font for the Treeview note selection text
custom_treeview_font = font.Font(family='Helvetica', size=14)  # Change 'size' to your desired font size

# Apply the custom font to the Treeview widget
style.configure('Gray.Treeview', font=custom_treeview_font)

window.configure(background='#2E2E2E')  # Set the window background color

# Create a frame to hold the note list and text area using ttk
frame = ttk.Frame(window, padding="5", style='Gray.TFrame')
frame.pack(expand=True, fill='both')

# List to store note titles and their content
notes = {}

# Function to load notes from a file
def load_notes():
    global notes
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            try:
                notes = json.load(file)
                print(f"Loaded notes: {notes}")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to load notes. Starting with empty notes.")
                notes = {}
    if not notes:
        notes["Untitled Note"] = ""  # Create a default note if no notes are present

# Function to save notes to a file
def save_notes():
    with open(SAVE_FILE, 'w') as file:
        json.dump(notes, file)
    print(f"Saved notes: {notes}")

# Load notes from the file when the program starts
load_notes()

# Combined toolbar at the top
toolbar = ttk.Frame(window, padding="5", style='Gray.TFrame')
toolbar.pack(side='top', fill='x')

# Create a PanedWindow to allow resizing between the list and text area
paned_window = ttk.PanedWindow(frame, orient='horizontal', style='Gray.TFrame')
paned_window.pack(expand=True, fill='both')

# Create a frame for the note list
list_frame = ttk.Frame(paned_window, style='Gray.TFrame')
paned_window.add(list_frame, weight=1)

# Create a Treeview to display note titles with scrollbar
note_tree = ttk.Treeview(list_frame, show='tree', selectmode='browse', style='Gray.Treeview')
note_tree.heading('#0', text='Notes', anchor='w')

# Populate the Treeview with loaded note titles
for note_title in notes:
    note_tree.insert('', 'end', text=note_title)

note_tree.pack(side='left', fill='both', expand=True)

# Add a vertical scrollbar to the note list
list_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=note_tree.yview, style='Vertical.Gray.TScrollbar')
note_tree.configure(yscrollcommand=list_scrollbar.set)
list_scrollbar.pack(side='right', fill='y')

# Create a Text widget where you can type your notes
text_frame = ttk.Frame(paned_window, style='Gray.TFrame')
paned_window.add(text_frame, weight=4)

# Create the text area with a scrollbar
text_area = tk.Text(text_frame, wrap='word', undo=True, background='#3C3C3C', foreground='#FFFFFF',
                    insertbackground='#FFFFFF', highlightthickness=0, borderwidth=0)
text_area.pack(expand=True, fill='both', side='left')

text_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_area.yview, style='Vertical.Gray.TScrollbar')
text_area.configure(yscrollcommand=text_scrollbar.set)
text_scrollbar.pack(side='right', fill='y')

# Apply the default font to the text area
text_area.configure(font=default_font)

# Variable to track the currently selected note title
current_note = None

# Function to display the content of the selected note
def show_note_content(event=None):
    global current_note
    # Save the current note's content before switching
    if current_note:
        save_current_note_content()

    # Get the selected note title from the Treeview
    selected_item = note_tree.focus()
    if selected_item:
        selected_note = note_tree.item(selected_item)['text']
        print(f"Switching to note: {selected_note}")

        # Set the current note to the selected note
        current_note = selected_note

        # Display the content of the selected note in the text area
        text_area.config(state='normal')  # Ensure the text area is editable
        text_area.delete(1.0, 'end')  # Clear the current text
        text_area.insert('end', notes[selected_note])  # Insert the content of the selected note
        text_area.config(state='normal')  # Keep the text area editable for the new content
    else:
        print("No note selected")

# Function to create a new note with a custom name
def create_new_note():
    global current_note
    # Prompt the user to enter a name for the new note
    new_note_title = simpledialog.askstring("New Note", "Enter the name of your new note:")
    if new_note_title and new_note_title not in notes:
        notes[new_note_title] = ""  # Add the new note to the dictionary
        note_tree.insert('', 'end', text=new_note_title)  # Insert the new note title in the Treeview
        note_tree.selection_set(note_tree.get_children()[-1])  # Select the new note
        show_note_content(None)  # Show content of the new note
        current_note = new_note_title  # Set the current note to the new note
    elif new_note_title in notes:
        messagebox.showerror("Error", f"A note with the name '{new_note_title}' already exists.")

# Function to save the current content of the selected note
def save_current_note_content():
    global current_note
    if current_note:
        # Update the content of the current note in the dictionary
        notes[current_note] = text_area.get(1.0, 'end').strip()
        print(f"Saved content for note '{current_note}': {notes[current_note]}")

# Function to delete the selected note
def delete_selected_note():
    global current_note
    selected_item = note_tree.focus()
    if selected_item:
        selected_note = note_tree.item(selected_item)['text']

        # Confirm deletion
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete the note '{selected_note}'?")
        if confirm:
            # Remove the note from the dictionary
            del notes[selected_note]

            # Remove the note from the Treeview
            note_tree.delete(selected_item)

            # Clear the text area and reset current note
            text_area.delete(1.0, 'end')
            current_note = None

            # Select another note if available, or show blank area if no notes left
            if note_tree.get_children():
                first_item = note_tree.get_children()[0]
                note_tree.selection_set(first_item)  # Select the first note
                show_note_content(None)
            else:
                notes["Untitled Note"] = ""  # Create a default blank note
                new_item = note_tree.insert('', 'end', text="Untitled Note")
                note_tree.selection_set(new_item)
                show_note_content(None)
    else:
        messagebox.showinfo("No Note Selected", "Please select a note to delete.")

# Function to create a hidden input box and get user input
def get_hidden_input():
    # Create a root window and hide it immediately
    root = tk.Tk()
    root.withdraw()

    # Create a tiny Toplevel window
    hidden_root = tk.Toplevel(root)
    hidden_root.geometry("1x1+0+0")  # Set the size to 1x1 pixels and position at the top-left corner

    # Hide the title bar to make it less visible
    hidden_root.overrideredirect(True)

    # Set the window to not be on top of other windows
    hidden_root.attributes("-topmost", False)

    # Lower the window so it doesn't appear in front of other windows
    hidden_root.lower()

    # Use the tiny or minimized window as the parent for the dialog
    user_question = simpledialog.askstring("Search", "", show=' ', parent=hidden_root)

    # Destroy the temporary window after getting input
    hidden_root.destroy()
    root.destroy()

    return user_question

# Function to call ask_chatgpt with user prompt and append the response to the previous note
def call_chatgpt(use_clipboard=False):
    global current_note
    if not current_note:
        messagebox.showinfo("No Note Selected", "Please select a note to proceed.")
        return

    if use_clipboard:
        user_question = pyperclip.paste()
        if not user_question:
            messagebox.showinfo("Empty Clipboard", "Your clipboard is empty. Please copy some text and try again.")
            return
    else:
        user_question = get_hidden_input()
        if not user_question:
            return

    # Call ask_chatgpt with the user question
    try:
        response = ask_chatgpt(user_question)  # Pass the question to the ask_chatgpt function in ai.py

        # Get a list of all note titles
        note_titles = list(notes.keys())
        # Find the index of the current note
        current_index = note_titles.index(current_note)

        # Check if there is a previous note
        if current_index > 0:
            previous_note = note_titles[current_index - 1]
            notes[previous_note] += "\n\n\n\n" + response
            print(f"Appended response to previous note: {previous_note}")
            # If the previous note is currently selected, update the text area
            if previous_note == current_note:
                text_area.insert('end', "\n\nResponse:\n" + response)
            elif current_note == previous_note:
                # Update the text area if the previous note is currently displayed
                text_area.delete(1.0, 'end')
                text_area.insert('end', notes[previous_note])
        else:
            messagebox.showinfo("No Previous Note", "There is no previous note to add the response to.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get response: {e}")

# Function to change the font size
def change_font_size(event=None):
    selected_font_size = font_size_combo.get()
    if selected_font_size:
        current_font = font.Font(font=text_area['font'])
        current_font.configure(size=int(selected_font_size))
        text_area.configure(font=current_font)

# Function to change the font family
def change_font_family(event=None):
    selected_font_family = font_family_combo.get()
    if selected_font_family:
        current_font = font.Font(font=text_area['font'])
        current_font.configure(family=selected_font_family)
        text_area.configure(font=current_font)

# Function to change the font color
def change_font_color():
    color_code = colorchooser.askcolor(title="Choose font color")
    if color_code and color_code[1]:
        text_area.tag_add("colored", "sel.first", "sel.last")
        text_area.tag_configure("colored", foreground=color_code[1])

# Function to highlight text
def highlight_text():
    color_code = colorchooser.askcolor(title="Choose highlight color")
    if color_code and color_code[1]:
        text_area.tag_add("highlight", "sel.first", "sel.last")
        text_area.tag_configure("highlight", background=color_code[1])

# Function to change line spacing
def change_line_spacing(spacing):
    text_area.tag_add("line_spacing", "sel.first", "sel.last")
    text_area.tag_configure("line_spacing", spacing1=spacing)

# Function to align text
def align_text(alignment):
    text_area.tag_add("alignment", "sel.first", "sel.last")
    text_area.tag_configure("alignment", justify=alignment)

# Function to make selected text bold
def make_bold():
    text_area.tag_add("bold", "sel.first", "sel.last")
    bold_font = font.Font(text_area, text_area.cget("font"))
    bold_font.configure(weight="bold")
    text_area.tag_configure("bold", font=bold_font)

# Function to make selected text italic
def make_italic():
    text_area.tag_add("italic", "sel.first", "sel.last")
    italic_font = font.Font(text_area, text_area.cget("font"))
    italic_font.configure(slant="italic")
    text_area.tag_configure("italic", font=italic_font)

# Function to underline text
def make_underline():
    text_area.tag_add("underline", "sel.first", "sel.last")
    underline_font = font.Font(text_area, text_area.cget("font"))
    underline_font.configure(underline=True)
    text_area.tag_configure("underline", font=underline_font)

# Function to strikethrough text
def make_strikethrough():
    text_area.tag_add("strikethrough", "sel.first", "sel.last")
    strikethrough_font = font.Font(text_area, text_area.cget("font"))
    strikethrough_font.configure(overstrike=True)
    text_area.tag_configure("strikethrough", font=strikethrough_font)

# Load icons (ensure you have these icon files in the same directory)
try:
    new_icon = tk.PhotoImage(file='icons/new.png')
    delete_icon = tk.PhotoImage(file='icons/delete.png')
    chatgpt_icon = tk.PhotoImage(file='icons/chatgpt.png')
    bold_icon = tk.PhotoImage(file='icons/bold.png')
    italic_icon = tk.PhotoImage(file='icons/italic.png')
    underline_icon = tk.PhotoImage(file='icons/underline.png')
    strikethrough_icon = tk.PhotoImage(file='icons/strikethrough.png')
    color_icon = tk.PhotoImage(file='icons/color.png')
    highlight_icon = tk.PhotoImage(file='icons/highlight.png')
    align_left_icon = tk.PhotoImage(file='icons/align_left.png')
    align_center_icon = tk.PhotoImage(file='icons/align_center.png')
    align_right_icon = tk.PhotoImage(file='icons/align_right.png')
    line_spacing_icon = tk.PhotoImage(file='icons/line_spacing.png')
except Exception as e:
    # If icon files are not found, use default text
    new_icon = None
    delete_icon = None
    chatgpt_icon = None
    bold_icon = None
    italic_icon = None
    underline_icon = None
    strikethrough_icon = None
    color_icon = None
    highlight_icon = None
    align_left_icon = None
    align_center_icon = None
    align_right_icon = None
    line_spacing_icon = None
    print(f"Icon loading error: {e}")

# Buttons with icons on the combined toolbar
# Left section of the toolbar
new_note_button = ttk.Button(toolbar, text="New Note", command=create_new_note, image=new_icon, compound='left', style='Gray.TButton')
new_note_button.pack(side='left', padx=2)

delete_note_button = ttk.Button(toolbar, text="Delete Note", command=delete_selected_note, image=delete_icon, compound='left', style='Gray.TButton')
delete_note_button.pack(side='left', padx=2)

chatgpt_button = ttk.Button(toolbar, text="Search", command=call_chatgpt, image=chatgpt_icon, compound='left', style='Gray.TButton')
chatgpt_button.pack(side='left', padx=2)

# Separator between sections
separator = ttk.Separator(toolbar, orient='vertical')
separator.pack(side='left', fill='y', padx=5)

# Right section of the toolbar (formatting options)
font_families = sorted(set(font.families()))
font_family_combo = ttk.Combobox(toolbar, values=font_families, width=15, style='Gray.TCombobox')
font_family_combo.set("Arial")  # Set default font family
font_family_combo.bind("<<ComboboxSelected>>", change_font_family)
font_family_combo.pack(side='left', padx=5)

font_sizes = [str(size) for size in range(8, 32, 2)]
font_size_combo = ttk.Combobox(toolbar, values=font_sizes, width=5, style='Gray.TCombobox')
font_size_combo.set("12")  # Set default font size
font_size_combo.bind("<<ComboboxSelected>>", change_font_size)
font_size_combo.pack(side='left', padx=5)

bold_button = ttk.Button(toolbar, text="Bold", command=make_bold, image=bold_icon, compound='left', style='Gray.TButton')
bold_button.pack(side='left', padx=2)

italic_button = ttk.Button(toolbar, text="Italic", command=make_italic, image=italic_icon, compound='left', style='Gray.TButton')
italic_button.pack(side='left', padx=2)

underline_button = ttk.Button(toolbar, text="Underline", command=make_underline, image=underline_icon, compound='left', style='Gray.TButton')
underline_button.pack(side='left', padx=2)

strikethrough_button = ttk.Button(toolbar, text="Strikethrough", command=make_strikethrough, image=strikethrough_icon, compound='left', style='Gray.TButton')
strikethrough_button.pack(side='left', padx=2)

color_button = ttk.Button(toolbar, text="Font Color", command=change_font_color, image=color_icon, compound='left', style='Gray.TButton')
color_button.pack(side='left', padx=2)

highlight_button = ttk.Button(toolbar, text="Highlight", command=highlight_text, image=highlight_icon, compound='left', style='Gray.TButton')
highlight_button.pack(side='left', padx=2)

# Alignment buttons
align_left_button = ttk.Button(toolbar, command=lambda: align_text('left'), image=align_left_icon, style='Gray.TButton')
align_left_button.pack(side='left', padx=2)

align_center_button = ttk.Button(toolbar, command=lambda: align_text('center'), image=align_center_icon, style='Gray.TButton')
align_center_button.pack(side='left', padx=2)

align_right_button = ttk.Button(toolbar, command=lambda: align_text('right'), image=align_right_icon, style='Gray.TButton')
align_right_button.pack(side='left', padx=2)

# Line spacing options
def set_line_spacing():
    spacing = simpledialog.askfloat("Line Spacing", "Enter line spacing (e.g., 1.0, 1.5, 2.0):", minvalue=0.5, maxvalue=4.0)
    if spacing:
        change_line_spacing(spacing)

line_spacing_button = ttk.Button(toolbar, text="Line Spacing", command=set_line_spacing, image=line_spacing_icon, compound='left', style='Gray.TButton')
line_spacing_button.pack(side='left', padx=2)

# Save the current note's content whenever a new note is selected
note_tree.bind("<<TreeviewSelect>>", show_note_content)

# Save notes when the window is closed
def on_closing():
    save_current_note_content()  # Save current note content
    save_notes()  # Save all notes to the file
    window.destroy()

# Configure the close window action
window.protocol("WM_DELETE_WINDOW", on_closing)

# Show the content of the first note by default if notes exist
if notes:
    first_item = note_tree.get_children()[0]
    note_tree.selection_set(first_item)
    show_note_content(None)

# Function to handle the backtick key press
def on_backtick_key(event):
    call_chatgpt(use_clipboard=True)

# Bind the backtick key to the call_chatgpt function without popping up an input box
window.bind("`", on_backtick_key)

# Start the main loop to display the window
window.mainloop()
