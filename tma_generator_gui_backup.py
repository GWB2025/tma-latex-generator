import re
import argparse
import datetime
import os
import textwrap
import json
from collections import defaultdict
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# PDF extraction functionality removed - using manual input only

class ToolTip:
    """Create a tooltip for a given widget."""
    def __init__(self, widget, text=''):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.tooltip_window = None

    def on_enter(self, event=None):
        if self.text:
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            
            self.tooltip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry("+%d+%d" % (x, y))
            
            label = tk.Label(tw, text=self.text, justify='left',
                           background='#ffffe0', relief='solid', borderwidth=1,
                           wraplength=300, font=("Arial", "9", "normal"))
            label.pack(ipadx=5, ipady=3)

    def on_leave(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_text(self, new_text):
        self.text = new_text

class HelpDialog:
    """Help dialog with comprehensive instructions and examples."""
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("TMA LaTeX Generator - Help")
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_help_content()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_help_content(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="TMA LaTeX Generator - User Guide", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Scrolled text widget for content
        text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                              font=("Arial", 10), height=30)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Help content
        help_content = self.get_help_content()
        text_widget.insert(tk.END, help_content)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.dialog.destroy)
        close_button.pack(pady=(5, 0))
    
    def get_help_content(self):
        return """
🎯 OVERVIEW

The TMA LaTeX Generator creates structured LaTeX files for academic assignments. You manually specify the question structure, and the application generates all necessary files organized for easy editing.

📋 STEP-BY-STEP GUIDE

1. BASIC SETTINGS
   • Course Code: Your module code (e.g., M840-AAT, M336, etc.)
   • TMA Reference: Assignment number (e.g., 01, 02, 03, 04)
   • Cut-off Date: Submission deadline (e.g., "15 January 2024")
   • Your Name: Your full name as registered
   • Student PIN: Your OU personal identification number
   • LaTeX Style: Style file to use (usually "tma")
   • Output Directory: Where to save generated files
   • Base Filename: Main file name (usually "TMA")

2. QUESTION STRUCTURE
   This is where you specify how your TMA is organized:

   📝 MARKS FIELD
   Enter the total marks for each question as a number.
   Examples: 25, 30, 15, 20

   📝 PARTS FIELD
   List question parts separated by commas.
   Examples:
   • "a,b,c,d" - for parts (a), (b), (c), (d)
   • "a,b" - for just parts (a), (b)
   • "a,b,c,d,e,f" - for six parts

   📝 SUBPARTS FIELD
   Specify subparts for each part using the format: part:subparts
   Multiple parts separated by semicolons.
   Examples:
   • "a:i,ii,iii" - part (a) has subparts (i), (ii), (iii)
   • "a:i,ii;c:i,ii,iii,iv" - part (a) has 2 subparts, part (c) has 4
   • "b:1,2,3" - part (b) has numbered subparts (1), (2), (3)
   • Leave blank if no subparts needed

3. COMPLETE EXAMPLES

   📚 EXAMPLE 1: Simple Question
   Question 1:
   • Marks: 25
   • Parts: a,b,c,d
   • Subparts: (leave blank)
   
   This creates: Q1 with parts (a), (b), (c), (d), no subparts

   📚 EXAMPLE 2: Complex Question
   Question 1:
   • Marks: 30
   • Parts: a,b,c
   • Subparts: a:i,ii,iii;c:i,ii
   
   This creates:
   • Q1(a) with subparts (i), (ii), (iii)
   • Q1(b) with no subparts
   • Q1(c) with subparts (i), (ii)

   📚 EXAMPLE 3: Mixed Numbering
   Question 2:
   • Marks: 20
   • Parts: a,b
   • Subparts: a:1,2,3,4;b:i,ii
   
   This creates:
   • Q2(a) with subparts (1), (2), (3), (4)
   • Q2(b) with subparts (i), (ii)

4. COMMON TMA PATTERNS

   🏫 TYPICAL OU TMA STRUCTURE:
   • 4 questions, 25 marks each
   • Each question has 4 parts (a,b,c,d)
   • Some parts may have subparts

   📖 EXAMPLE TMA SETUP:
   
   Question 1: Marks=25, Parts=a,b,c,d, Subparts=a:i,ii;c:i,ii,iii
   Question 2: Marks=25, Parts=a,b,c,d, Subparts=b:i,ii,iii
   Question 3: Marks=25, Parts=a,b,c,d, Subparts=(blank)
   Question 4: Marks=25, Parts=a,b,c,d, Subparts=d:i,ii

5. GENERATED FILES

   The application creates:
   • Main LaTeX file (TMA.tex)
   • Question files (q1.tex, q2.tex, etc.)
   • Part files (q1a.tex, q1b.tex, etc.)
   • Subpart files (q1a_0.tex, q1a_1.tex, etc.)

6. CONTROLS

   🔧 BUTTONS:
   • Add Question: Creates a new question entry
   • Clear All: Removes all questions (use carefully!)
   • Generate TMA Files: Creates the LaTeX file structure
   • Save Settings: Saves your configuration for next time
   • Help: Shows this help dialog

   ⚠️ TIPS:
   • Start with one question to test your setup
   • Save settings frequently to avoid re-entering information
   • Check the output directory exists before generating
   • Review the generated structure in the output log

7. TROUBLESHOOTING

   ❌ Common Issues:
   • "No questions specified": Add at least one question
   • "Invalid marks": Enter numbers only in marks field
   • "Directory error": Check output directory path is valid
   • "Generation failed": Check all fields are properly filled

   ✅ Best Practices:
   • Use consistent naming (lowercase for parts: a,b,c)
   • Check subpart syntax carefully (part:sub1,sub2)
   • Test with simple structure first
   • Keep backup of your LaTeX style files

📞 NEED MORE HELP?

This tool generates the file structure. You'll need:
• A LaTeX editor (TeXstudio, TeXworks, etc.)
• Your university's LaTeX style file (tma.sty)
• Basic LaTeX knowledge for content editing

The generated files provide the framework - you add your actual answers and mathematical content in each part file.
        """

# Configuration file path
CONFIG_FILE = "tma_generator_config.json"

def load_config():
    """Load configuration from file."""
    default_config = {
        "course": "MATH101",
        "tma_ref": "04",
        "cod": "??",
        "name": "John Smith",
        "pin": "S1234567",
        "style": "tma",
        "output": "./output",
        "basename": "TMA"
    }
    
    try:
        if Path(CONFIG_FILE).exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    
    return default_config

def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass

# PDF extraction functions removed - using manual input only


# LaTeX generation functions (same as before)
def create_directory(directory):
    """Create a directory, handling existing directories by renaming with timestamp."""
    directory_path = Path(directory).resolve()
    
    try:
        directory_path.mkdir(parents=True, exist_ok=False)
        return str(directory_path)
    except FileExistsError:
        now = datetime.datetime.now()
        timestamp = f"{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}"
        new_directory = f"{directory_path}.{timestamp}"
        
        print(f'Directory {directory_path} exists so renaming it to {new_directory}')
        os.rename(directory_path, new_directory)
        directory_path.mkdir(parents=True)
        return str(directory_path)

def create_main_tex_file(folder, basename, number_of_questions, course, tma_ref, cod, name, pin, style='tma'):
    """Create the main LaTeX document file."""
    try:
        file_path = Path(folder) / (basename + '.tex')
        content = create_main_tex_content(
            name=name, pin=pin, tma_ref=tma_ref, number_of_questions=number_of_questions, 
            cod=cod, course=course, style=style
        )
        
        with open(file_path, 'w+', encoding='utf-8') as f:
            f.write(textwrap.dedent(content)[1:])
            
    except Exception as e:
        raise Exception(f"Error creating main LaTeX file: {e}")

def create_main_tex_content(style='tma', name='John Smith', pin='M1234567', course='M836',
                           tma_ref='02', cod='11 January 2023', number_of_questions=4):
    """Generate the content for the main LaTeX document."""
    lines = '%%!TEX TS-program = pythontex\n'
    lines += '\\documentclass[a4paper,12pt]{article}\n'
    lines += '\\usepackage{{{}}}\n'.format(style)
    lines += '\\myname{{{}}}\n'.format(name)
    lines += '\\mypin{{{}}}\n'.format(pin)
    lines += '\\mycourse{{{}}}\n'.format(course)
    lines += '\\mytma{{{}}}\n'.format(tma_ref)
    lines += '\\mycod{{{}}}\n\n'.format(cod)

    line = '\\includeonly{'
    for i in range(number_of_questions):
        line += 'q' + str(i + 1) + ','
    line = line.rstrip(',')
    line += '}\n'
    lines += line
    
    lines += '\\begin{document}\n'
    for i in range(number_of_questions):
        lines += '\t\\include{{{}}}\n'.format('q' + str(i + 1))
    lines += '\\end{document}\n'
    
    return lines

def create_question(folder, basename, question_number, question_parts):
    """Create LaTeX question files with subparts."""
    try:
        folder_path = Path(folder)
        
        question_content = ''
        question_content += '% !TeX root = ./{}.tex\n'.format(basename)
        question_content += '\\begin{question}\n'
        
        for i in range(0, len(question_parts)):
            question_content += '\t\\qpart %({})\n'.format(chr(97 + i))
            question_content += '\t\\input{{{}}}\n'.format('q' + question_number + chr(97 + i))
            
            part_filename = folder_path / ('q' + question_number + chr(97 + i) + '.tex')
            with open(part_filename, 'w+', encoding='utf-8') as f1:
                f1.write('% !TeX root = ./{}.tex'.format(basename))
                
        question_content += '\\end{question}'
        
        question_filename = folder_path / ('q' + question_number + '.tex')
        with open(question_filename, 'w+', encoding='utf-8') as f:
            f.write(question_content)
            
    except Exception as e:
        raise Exception(f"Error creating question files: {e}")

def create_subparts(folder, basename, subparts_dict):
    """Create additional subparts for existing questions."""
    try:
        folder_path = Path(folder)
        
        for key, num_subparts in subparts_dict.items():
            filename = folder_path / (key + '.tex')
            
            if filename.exists():
                with open(filename, 'a', encoding='utf-8') as f:
                    lines = ''
                    for i in range(num_subparts):
                        lines += '\n\\qsubpart'
                        lines += '\n\\input{{{}}}'.format(key + '_' + str(i))
                        
                        subpart_filename = folder_path / (key + '_' + str(i) + '.tex')
                        with open(subpart_filename, 'w+', encoding='utf-8') as f2:
                            f2.write('% !TeX root = ./{}.tex\n'.format(basename))
                    
                    f.write(lines)
    except Exception as e:
        raise Exception(f"Error creating subparts: {e}")


def generate_tma_files_manual(config, structure, output_text=None):
    """Generate TMA files based on manual structure input."""
    try:
        if output_text:
            output_text.insert(tk.END, "Using manual question structure...\n")
            output_text.see(tk.END)
            output_text.update()
        
        if output_text:
            output_text.insert(tk.END, "Question Structure:\n")
            for q_id, q_data in sorted(structure.items(), key=lambda x: int(x[0][1:])):
                marks = q_data.get('marks', 'N/A')
                output_text.insert(tk.END, f"{q_id}: {marks} marks\n")
                
                for part_id in sorted(q_data.get('parts', {}).keys()):
                    output_text.insert(tk.END, f"  ({part_id})\n")
                    
                    subparts = q_data['parts'][part_id].get('subparts', {})
                    for subpart_id in sorted(subparts.keys()):
                        output_text.insert(tk.END, f"    ({subpart_id})\n")
            output_text.see(tk.END)
            output_text.update()
        
        # Prepare data for LaTeX generation
        number_of_questions = len(structure)
        parts = []
        subparts_dict = {}
        
        for q_id in sorted(structure.keys(), key=lambda x: int(x[1:])):
            q_data = structure[q_id]
            question_parts = tuple(sorted(q_data.get('parts', {}).keys()))
            parts.append(question_parts)
            
            for part_id, part_data in q_data.get('parts', {}).items():
                subparts = list(part_data.get('subparts', {}).keys())
                if subparts:
                    subparts_dict[f'q{q_id[1:]}{part_id}'] = len(subparts)
        
        # Create the directory
        actual_folder = create_directory(config["output"])
        
        if output_text:
            output_text.insert(tk.END, f"Created directory: {actual_folder}\n")
            output_text.see(tk.END)
            output_text.update()
        
        # Create the main LaTeX file
        create_main_tex_file(
            folder=actual_folder, 
            basename=config["basename"], 
            number_of_questions=number_of_questions, 
            course=config["course"], 
            tma_ref=config["tma_ref"], 
            cod=config["cod"],
            name=config["name"],
            pin=config["pin"],
            style=config["style"]
        )
        
        # Create question files
        for i, question_parts in enumerate(parts):
            create_question(actual_folder, config["basename"], str(i + 1), question_parts)
        
        # Create subparts if any
        if subparts_dict:
            create_subparts(actual_folder, config["basename"], subparts_dict)
        
        success_message = f"TMA files successfully created in {actual_folder}"
        if output_text:
            output_text.insert(tk.END, f"{success_message}\n")
            output_text.insert(tk.END, "Generation completed successfully!\n")
            output_text.see(tk.END)
        
        return True, success_message
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        if output_text:
            output_text.insert(tk.END, f"{error_message}\n")
            output_text.see(tk.END)
        return False, error_message

class TMAGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TMA LaTeX Generator")
        self.root.geometry("800x900")  # Increased size for manual input section
        
        # Load configuration
        self.config = load_config()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="TMA LaTeX Generator", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input fields
        row = 2
        
        # Course Code
        ttk.Label(main_frame, text="Course Code:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.course_var = tk.StringVar(value=self.config["course"])
        course_entry = ttk.Entry(main_frame, textvariable=self.course_var, width=15)
        course_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(course_entry, "Your module code (e.g., MATH101, PHYS201)")
        row += 1
        
        # TMA Reference
        ttk.Label(main_frame, text="TMA Reference:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.tma_ref_var = tk.StringVar(value=self.config["tma_ref"])
        tma_ref_entry = ttk.Entry(main_frame, textvariable=self.tma_ref_var, width=10)
        tma_ref_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(tma_ref_entry, "TMA assignment number (e.g., 01, 02, 03, 04)")
        row += 1
        
        # Cut-off Date
        ttk.Label(main_frame, text="Cut-off Date:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.cod_var = tk.StringVar(value=self.config["cod"])
        cod_entry = ttk.Entry(main_frame, textvariable=self.cod_var, width=15)
        cod_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(cod_entry, "Assignment submission deadline (e.g., '15 January 2024', 'TBD')")
        row += 1
        
        # Name
        ttk.Label(main_frame, text="Your Name:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar(value=self.config["name"])
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(name_entry, "Your full name as registered with your institution")
        row += 1
        
        # PIN
        ttk.Label(main_frame, text="Student PIN:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.pin_var = tk.StringVar(value=self.config["pin"])
        pin_entry = ttk.Entry(main_frame, textvariable=self.pin_var, width=15)
        pin_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(pin_entry, "Your OU Personal Identification Number (e.g., M1234567)")
        row += 1
        
        # Style
        ttk.Label(main_frame, text="LaTeX Style:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.style_var = tk.StringVar(value=self.config["style"])
        style_entry = ttk.Entry(main_frame, textvariable=self.style_var, width=10)
        style_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(style_entry, "LaTeX style file to use (usually 'tma' for academic assignments)")
        row += 1
        
        # Output Directory
        ttk.Label(main_frame, text="Output Directory:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.output_var = tk.StringVar(value=self.config["output"])
        output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=30)
        output_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        ToolTip(output_entry, "Directory where LaTeX files will be created. Use Browse button or type path directly.")
        browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_output)
        browse_button.grid(row=row, column=2, pady=2, padx=(5, 0))
        ToolTip(browse_button, "Click to select output directory")
        row += 1
        
        # Base Filename
        ttk.Label(main_frame, text="Base Filename:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.basename_var = tk.StringVar(value=self.config["basename"])
        basename_entry = ttk.Entry(main_frame, textvariable=self.basename_var, width=15)
        basename_entry.grid(row=row, column=1, sticky=tk.W, pady=2, padx=(5, 0))
        ToolTip(basename_entry, "Name for main LaTeX file (usually 'TMA'). Creates TMA.tex as main file.")
        row += 1
        
        # Separator for Question Structure section
        separator3 = ttk.Separator(main_frame, orient='horizontal')
        separator3.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # Question Structure section
        structure_label = ttk.Label(main_frame, text="Question Structure (Manual Input)", font=("Arial", 12, "bold"))
        structure_label.grid(row=row, column=0, columnspan=3, pady=(0, 5))
        row += 1
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=row, column=0, columnspan=3, pady=5)
        
        clear_button = ttk.Button(control_frame, text="Clear All", command=self.clear_structure)
        clear_button.pack(side=tk.LEFT, padx=5)
        ToolTip(clear_button, "Remove all questions from the structure (cannot be undone!)")
        
        add_button = ttk.Button(control_frame, text="Add Question", command=self.add_question)
        add_button.pack(side=tk.LEFT, padx=5)
        ToolTip(add_button, "Add a new question to the structure")
        
        help_button = ttk.Button(control_frame, text="Help", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=5)
        ToolTip(help_button, "Show comprehensive help with examples and instructions")
        
        row += 1
        
        # Scrollable frame for question structure
        self.structure_canvas = tk.Canvas(main_frame, height=200)
        self.structure_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.structure_canvas.yview)
        self.structure_scrollable_frame = ttk.Frame(self.structure_canvas)
        
        self.structure_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all"))
        )
        
        self.structure_canvas.create_window((0, 0), window=self.structure_scrollable_frame, anchor="nw")
        self.structure_canvas.configure(yscrollcommand=self.structure_scrollbar.set)
        
        self.structure_canvas.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        self.structure_scrollbar.grid(row=row, column=2, sticky=(tk.N, tk.S), pady=(5, 0))
        row += 1
        
        # Initialize question structure storage
        self.question_widgets = []
        self.add_question()  # Add first question by default
        
        # Separator
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        generate_button = ttk.Button(button_frame, text="Generate TMA Files", command=self.generate_files)
        generate_button.pack(side=tk.LEFT, padx=5)
        ToolTip(generate_button, "Create the LaTeX file structure based on your question setup")
        
        save_button = ttk.Button(button_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(side=tk.LEFT, padx=5)
        ToolTip(save_button, "Save your current configuration to avoid re-entering next time")
        
        exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.LEFT, padx=5)
        ToolTip(exit_button, "Close the application")
        
        row += 1
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=row, column=0, sticky=tk.W, pady=(10, 0))
        row += 1
        
        self.output_text = scrolledtext.ScrolledText(main_frame, width=70, height=15)
        self.output_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def browse_output(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
    
    def show_help(self):
        """Show the help dialog."""
        HelpDialog(self.root)
    
    def save_settings(self):
        self.config = {
            "course": self.course_var.get(),
            "tma_ref": self.tma_ref_var.get(),
            "cod": self.cod_var.get(),
            "name": self.name_var.get(),
            "pin": self.pin_var.get(),
            "style": self.style_var.get(),
            "output": self.output_var.get(),
            "basename": self.basename_var.get()
        }
        save_config(self.config)
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
    
    def add_question(self):
        """Add a new question to the structure input."""
        question_num = len(self.question_widgets) + 1
        question_frame = ttk.LabelFrame(self.structure_scrollable_frame, text=f"Question {question_num}")
        question_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Question details frame
        details_frame = ttk.Frame(question_frame)
        details_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Marks input
        ttk.Label(details_frame, text="Marks:").pack(side=tk.LEFT)
        marks_var = tk.StringVar(value="25")
        marks_entry = ttk.Entry(details_frame, textvariable=marks_var, width=5)
        marks_entry.pack(side=tk.LEFT, padx=(2, 10))
        ToolTip(marks_entry, "Total marks for this question (e.g., 25, 30, 15)")
        
        # Parts input
        ttk.Label(details_frame, text="Parts:").pack(side=tk.LEFT)
        parts_var = tk.StringVar(value="a,b,c,d")
        parts_entry = ttk.Entry(details_frame, textvariable=parts_var, width=20)
        parts_entry.pack(side=tk.LEFT, padx=(2, 10))
        ToolTip(parts_entry, "Question parts separated by commas\nExamples: 'a,b,c,d' or 'a,b' or 'a,b,c,d,e,f'")
        
        # Subparts input
        ttk.Label(details_frame, text="Subparts (part:subparts):").pack(side=tk.LEFT)
        subparts_var = tk.StringVar(value="")
        subparts_entry = ttk.Entry(details_frame, textvariable=subparts_var, width=15)
        subparts_entry.pack(side=tk.LEFT, padx=(2, 10))
        ToolTip(subparts_entry, "Subparts for each part using format: part:sub1,sub2\nExamples:\n'a:i,ii,iii' or 'a:i,ii;c:1,2,3'\nLeave blank if no subparts")
        
        # Remove button
        remove_button = ttk.Button(details_frame, text="Remove", 
                                  command=lambda: self.remove_question(question_frame))
        remove_button.pack(side=tk.RIGHT)
        ToolTip(remove_button, "Remove this question from the structure")
        
        # Store references
        question_data = {
            'frame': question_frame,
            'marks_var': marks_var,
            'parts_var': parts_var,
            'subparts_var': subparts_var
        }
        self.question_widgets.append(question_data)
        
        # Update scroll region
        self.structure_canvas.update_idletasks()
        self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all"))
    
    def remove_question(self, question_frame):
        """Remove a question from the structure input."""
        # Find and remove from widgets list
        self.question_widgets = [q for q in self.question_widgets if q['frame'] != question_frame]
        question_frame.destroy()
        
        # Renumber remaining questions
        for i, question_data in enumerate(self.question_widgets):
            question_data['frame'].configure(text=f"Question {i + 1}")
        
        # Update scroll region
        self.structure_canvas.update_idletasks()
        self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all"))
    
    def clear_structure(self):
        """Clear all questions from the structure input."""
        for question_data in self.question_widgets:
            question_data['frame'].destroy()
        self.question_widgets = []
        
        # Update scroll region
        self.structure_canvas.update_idletasks()
        self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all"))
    
    def get_manual_structure(self):
        """Get the question structure from manual input."""
        structure = {}
        
        for i, question_data in enumerate(self.question_widgets):
            q_id = f"Q{i + 1}"
            
            # Get marks
            try:
                marks = int(question_data['marks_var'].get() or 25)
            except ValueError:
                marks = 25
            
            # Get parts
            parts_text = question_data['parts_var'].get().strip()
            parts = [p.strip() for p in parts_text.split(',') if p.strip()]
            
            # Get subparts
            subparts_text = question_data['subparts_var'].get().strip()
            subparts_dict = {}
            
            if subparts_text:
                for part_subparts in subparts_text.split(';'):
                    if ':' in part_subparts:
                        part, subparts_str = part_subparts.split(':', 1)
                        part = part.strip()
                        subparts = [s.strip() for s in subparts_str.split(',') if s.strip()]
                        subparts_dict[part] = {s: True for s in subparts}
            
            # Build structure
            structure[q_id] = {
                'marks': marks,
                'parts': {}
            }
            
            for part in parts:
                structure[q_id]['parts'][part] = {
                    'subparts': subparts_dict.get(part, {})
                }
        
        return structure
    
    def generate_files(self):
        # Clear output text
        self.output_text.delete(1.0, tk.END)
        
        # Update config with current values
        config = {
            "course": self.course_var.get(),
            "tma_ref": self.tma_ref_var.get(),
            "cod": self.cod_var.get(),
            "name": self.name_var.get(),
            "pin": self.pin_var.get(),
            "style": self.style_var.get(),
            "output": self.output_var.get(),
            "basename": self.basename_var.get()
        }
        
        # Get manual structure
        manual_structure = self.get_manual_structure()
        
        # Generate files using manual structure
        success, message = generate_tma_files_manual(config, manual_structure, self.output_text)
        
        if success:
            # Save successful settings
            self.config = config
            save_config(self.config)
            messagebox.showinfo("Success", "TMA files generated successfully!")
        else:
            messagebox.showerror("Error", message)

def main():
    """Main function - GUI only since PDF processing has been removed."""
    try:
        root = tk.Tk()
        app = TMAGeneratorGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")
        print("Error starting GUI. Please check tkinter installation.")

if __name__ == "__main__":
    main()