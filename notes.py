import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser, font
import json
import os
from tkinter import ttk
import pyperclip


from ai import ask_chatgpt

SAVE_FILE = os.path.join(os.getcwd(), "notes.json")

window = tk.Tk()
window.title("CS3530 Notes")
window.geometry("800x600") 
window.minsize(600, 400) 

style = ttk.Style()
style.theme_use('clam')  

default_font = font.Font(family='Arial', size=12)
treeview_font = font.Font(family='Helvetica', size=10)

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
custom_treeview_font = font.Font(family='Helvetica', size=14) 

style.configure('Gray.Treeview', font=custom_treeview_font)

window.configure(background='#2E2E2E') 

frame = ttk.Frame(window, padding="5", style='Gray.TFrame')
frame.pack(expand=True, fill='both')

notes = {}

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
        notes["Untitled Note"] = ""  

def save_notes():
    with open(SAVE_FILE, 'w') as file:
        json.dump(notes, file)
    print(f"Saved notes: {notes}")

load_notes()

toolbar = ttk.Frame(window, padding="5", style='Gray.TFrame')
toolbar.pack(side='top', fill='x')

paned_window = ttk.PanedWindow(frame, orient='horizontal', style='Gray.TFrame')
paned_window.pack(expand=True, fill='both')

list_frame = ttk.Frame(paned_window, style='Gray.TFrame')
paned_window.add(list_frame, weight=1)

note_tree = ttk.Treeview(list_frame, show='tree', selectmode='browse', style='Gray.Treeview')
note_tree.heading('#0', text='Notes', anchor='w')

for note_title in notes:
    note_tree.insert('', 'end', text=note_title)

note_tree.pack(side='left', fill='both', expand=True)

list_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=note_tree.yview, style='Vertical.Gray.TScrollbar')
note_tree.configure(yscrollcommand=list_scrollbar.set)
list_scrollbar.pack(side='right', fill='y')

text_frame = ttk.Frame(paned_window, style='Gray.TFrame')
paned_window.add(text_frame, weight=4)

text_area = tk.Text(text_frame, wrap='word', undo=True, background='#3C3C3C', foreground='#FFFFFF',
                    insertbackground='#FFFFFF', highlightthickness=0, borderwidth=0)
text_area.pack(expand=True, fill='both', side='left')

text_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_area.yview, style='Vertical.Gray.TScrollbar')
text_area.configure(yscrollcommand=text_scrollbar.set)
text_scrollbar.pack(side='right', fill='y')

text_area.configure(font=default_font)

current_note = None

def show_note_content(event=None):
    global current_note
    if current_note:
        save_current_note_content()

    selected_item = note_tree.focus()
    if selected_item:
        selected_note = note_tree.item(selected_item)['text']
        print(f"Switching to note: {selected_note}")

        current_note = selected_note

        text_area.config(state='normal')  
        text_area.delete(1.0, 'end')  
        text_area.insert('end', notes[selected_note])  
        text_area.config(state='normal')  
    else:
        print("No note selected")

def create_new_note():
    global current_note
    new_note_title = simpledialog.askstring("New Note", "Enter the name of your new note:")
    if new_note_title and new_note_title not in notes:
        notes[new_note_title] = ""  
        note_tree.insert('', 'end', text=new_note_title)  
        note_tree.selection_set(note_tree.get_children()[-1])  
        show_note_content(None)  
        current_note = new_note_title  
    elif new_note_title in notes:
        messagebox.showerror("Error", f"A note with the name '{new_note_title}' already exists.")

def save_current_note_content():
    global current_note
    if current_note:
        notes[current_note] = text_area.get(1.0, 'end').strip()
        print(f"Saved content for note '{current_note}': {notes[current_note]}")

def delete_selected_note():
    global current_note
    selected_item = note_tree.focus()
    if selected_item:
        selected_note = note_tree.item(selected_item)['text']

        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete the note '{selected_note}'?")
        if confirm:
            del notes[selected_note]

            note_tree.delete(selected_item)

            text_area.delete(1.0, 'end')
            current_note = None

            if note_tree.get_children():
                first_item = note_tree.get_children()[0]
                note_tree.selection_set(first_item) 
                show_note_content(None)
            else:
                notes["Untitled Note"] = ""  
                new_item = note_tree.insert('', 'end', text="Untitled Note")
                note_tree.selection_set(new_item)
                show_note_content(None)
    else:
        messagebox.showinfo("No Note Selected", "Please select a note to delete.")

def get_hidden_input():
    root = tk.Tk()
    root.withdraw()

    hidden_root = tk.Toplevel(root)
    hidden_root.geometry("1x1+0+0")  

    hidden_root.overrideredirect(True)

    hidden_root.attributes("-topmost", False)

    hidden_root.lower()

    user_question = simpledialog.askstring("Search", "", show=' ', parent=hidden_root)

    hidden_root.destroy()
    root.destroy()

    return user_question

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

    try:
        response = ask_chatgpt(user_question) 

        note_titles = list(notes.keys())
        current_index = note_titles.index(current_note)

        if current_index > 0:
            previous_note = note_titles[current_index - 1]
            notes[previous_note] += "\n\n\n\n" + response
            print(f"Appended response to previous note: {previous_note}")
            if previous_note == current_note:
                text_area.insert('end', "\n\nResponse:\n" + response)
            elif current_note == previous_note:
                text_area.delete(1.0, 'end')
                text_area.insert('end', notes[previous_note])
        else:
            messagebox.showinfo("No Previous Note", "There is no previous note to add the response to.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get response: {e}")

def change_font_size(event=None):
    selected_font_size = font_size_combo.get()
    if selected_font_size:
        current_font = font.Font(font=text_area['font'])
        current_font.configure(size=int(selected_font_size))
        text_area.configure(font=current_font)

def change_font_family(event=None):
    selected_font_family = font_family_combo.get()
    if selected_font_family:
        current_font = font.Font(font=text_area['font'])
        current_font.configure(family=selected_font_family)
        text_area.configure(font=current_font)

def change_font_color():
    color_code = colorchooser.askcolor(title="Choose font color")
    if color_code and color_code[1]:
        text_area.tag_add("colored", "sel.first", "sel.last")
        text_area.tag_configure("colored", foreground=color_code[1])

def highlight_text():
    color_code = colorchooser.askcolor(title="Choose highlight color")
    if color_code and color_code[1]:
        text_area.tag_add("highlight", "sel.first", "sel.last")
        text_area.tag_configure("highlight", background=color_code[1])

def change_line_spacing(spacing):
    text_area.tag_add("line_spacing", "sel.first", "sel.last")
    text_area.tag_configure("line_spacing", spacing1=spacing)

def align_text(alignment):
    text_area.tag_add("alignment", "sel.first", "sel.last")
    text_area.tag_configure("alignment", justify=alignment)

def make_bold():
    text_area.tag_add("bold", "sel.first", "sel.last")
    bold_font = font.Font(text_area, text_area.cget("font"))
    bold_font.configure(weight="bold")
    text_area.tag_configure("bold", font=bold_font)

def make_italic():
    text_area.tag_add("italic", "sel.first", "sel.last")
    italic_font = font.Font(text_area, text_area.cget("font"))
    italic_font.configure(slant="italic")
    text_area.tag_configure("italic", font=italic_font)

def make_underline():
    text_area.tag_add("underline", "sel.first", "sel.last")
    underline_font = font.Font(text_area, text_area.cget("font"))
    underline_font.configure(underline=True)
    text_area.tag_configure("underline", font=underline_font)

def make_strikethrough():
    text_area.tag_add("strikethrough", "sel.first", "sel.last")
    strikethrough_font = font.Font(text_area, text_area.cget("font"))
    strikethrough_font.configure(overstrike=True)
    text_area.tag_configure("strikethrough", font=strikethrough_font)

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


new_note_button = ttk.Button(toolbar, text="New Note", command=create_new_note, image=new_icon, compound='left', style='Gray.TButton')
new_note_button.pack(side='left', padx=2)

delete_note_button = ttk.Button(toolbar, text="Delete Note", command=delete_selected_note, image=delete_icon, compound='left', style='Gray.TButton')
delete_note_button.pack(side='left', padx=2)

chatgpt_button = ttk.Button(toolbar, text="Search", command=call_chatgpt, image=chatgpt_icon, compound='left', style='Gray.TButton')
chatgpt_button.pack(side='left', padx=2)

separator = ttk.Separator(toolbar, orient='vertical')
separator.pack(side='left', fill='y', padx=5)

font_families = sorted(set(font.families()))
font_family_combo = ttk.Combobox(toolbar, values=font_families, width=15, style='Gray.TCombobox')
font_family_combo.set("Arial")  
font_family_combo.bind("<<ComboboxSelected>>", change_font_family)
font_family_combo.pack(side='left', padx=5)

font_sizes = [str(size) for size in range(8, 32, 2)]
font_size_combo = ttk.Combobox(toolbar, values=font_sizes, width=5, style='Gray.TCombobox')
font_size_combo.set("12")  
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

align_left_button = ttk.Button(toolbar, command=lambda: align_text('left'), image=align_left_icon, style='Gray.TButton')
align_left_button.pack(side='left', padx=2)

align_center_button = ttk.Button(toolbar, command=lambda: align_text('center'), image=align_center_icon, style='Gray.TButton')
align_center_button.pack(side='left', padx=2)

align_right_button = ttk.Button(toolbar, command=lambda: align_text('right'), image=align_right_icon, style='Gray.TButton')
align_right_button.pack(side='left', padx=2)

def set_line_spacing():
    spacing = simpledialog.askfloat("Line Spacing", "Enter line spacing (e.g., 1.0, 1.5, 2.0):", minvalue=0.5, maxvalue=4.0)
    if spacing:
        change_line_spacing(spacing)

line_spacing_button = ttk.Button(toolbar, text="Line Spacing", command=set_line_spacing, image=line_spacing_icon, compound='left', style='Gray.TButton')
line_spacing_button.pack(side='left', padx=2)

note_tree.bind("<<TreeviewSelect>>", show_note_content)

def on_closing():
    save_current_note_content()  
    save_notes()  
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

if notes:
    first_item = note_tree.get_children()[0]
    note_tree.selection_set(first_item)
    show_note_content(None)

def on_backtick_key(event):
    call_chatgpt(use_clipboard=True)

window.bind("`", on_backtick_key)

window.mainloop()
