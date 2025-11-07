#!/usr/bin/env python3
"""
TMA LaTeX Generator GUI Application.

This application creates structured LaTeX files for academic TMA 
assignments. Users manually specify question structure through a graphical
interface, and the application generates all necessary LaTeX files organized
for easy editing.

Author: Generated for academic TMA workflow
Version: 2.0
Licence: MIT
"""

import argparse
import datetime
import json
import os
import re
import shutil
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext


# Configuration constants
CONFIG_FILE = "tma_generator_config.json"
DEFAULT_WINDOW_SIZE = "800x900"
TOOLTIP_DELAY_MS = 500
TOOLTIP_STYLE = {
    'background': '#ffffe0',
    'relief': 'solid',
    'borderwidth': 1,
    'wraplength': 300,
    'font': ("Arial", "9", "normal")
}

# Default configuration values
DEFAULT_CONFIG = {
    "course": "MATH101",
    "tma_ref": "04", 
    "cod": "21 January 2026",
    "title": "",
    "name": "Alex Noel Other",
    "pin": "S1234567",
    "style": "ou-tma",
    "output": "./output",
    "basename": "TMA",
    "part_numbering_style": "alph"
}

# GUI styling constants
MAIN_FRAME_PADDING = "10"
BUTTON_PADX = 5
ENTRY_PADY = 2
SEPARATOR_PADY = 10

# LaTeX file generation constants
TEX_EXTENSION = ".tex"
QUESTION_PREFIX = "q"
MAIN_TEX_PROGRAM = ""


class ToolTip:
    """
    Create a tooltip for any tkinter widget.
    
    Provides hover tooltips that display helpful information about widgets.
    Tooltips appear when mouse enters widget and disappear when mouse leaves.
    """
    
    def __init__(self, widget: tk.Widget, text: str = '') -> None:
        self.widget = widget
        self.text = text
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event: Optional[tk.Event] = None) -> None:
        if not self.text:
            return
        try:
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
        except tk.TclError:
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 25
        self.tooltip_window = tooltip = tk.Toplevel(self.widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tooltip, text=self.text, justify='left', **TOOLTIP_STYLE)
        label.pack(ipadx=5, ipady=3)
    
    def on_leave(self, event: Optional[tk.Event] = None) -> None:
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def update_text(self, new_text: str) -> None:
        self.text = new_text


class HelpDialog:
    """
    Comprehensive help dialog with usage instructions and examples.
    """
    
    def __init__(self, parent: tk.Widget) -> None:
        self.dialog = tk.Toplevel(parent)
        self._setup_dialog(parent)
        self._create_help_content()
        self._center_dialog()
    
    def _setup_dialog(self, parent: tk.Widget) -> None:
        self.dialog.title("TMA LaTeX Generator - Help")
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def _center_dialog(self) -> None:
        self.dialog.update_idletasks()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        dialogue_width = self.dialog.winfo_width()
        dialogue_height = self.dialog.winfo_height()
        x = (screen_width // 2) - (dialogue_width // 2)
        y = (screen_height // 2) - (dialogue_height // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_help_content(self) -> None:
        main_frame = ttk.Frame(self.dialog, padding=MAIN_FRAME_PADDING)
        main_frame.pack(fill=tk.BOTH, expand=True)
        title_label = ttk.Label(main_frame, text="TMA LaTeX Generator - User Guide", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Arial", 10), height=30)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        help_content = self._get_help_content()
        text_widget.insert(tk.END, help_content)
        text_widget.config(state=tk.DISABLED)
        close_button = ttk.Button(main_frame, text="Close", command=self.dialog.destroy)
        close_button.pack(pady=(5, 0))
    
    def _get_help_content(self) -> str:
        return """🎯 OVERVIEW

The TMA LaTeX Generator creates structured LaTeX files for academic assignments, specifically designed for Overleaf. You manually specify the question structure, and the application generates all necessary files organised for easy editing and upload to Overleaf.

📋 STEP-BY-STEP GUIDE

1. BASIC SETTINGS
   • Course Code: Your module code (e.g., M101, PHYS201, etc.)
   • TMA Reference: Assignment number (e.g., 01, 02, 03, 04)
   • Cut-off Date: Submission deadline (e.g., "21 January 2026")
   • Your Name: Your full name as registered (e.g., Alex Noel Other)
   • Student PIN: Your student identification number
   • LaTeX Style: The LaTeX style file to use. This is set to 'ou-tma' and cannot be changed.
   • Output Directory: Where to save generated files
   • Base Filename: Main file name (usually "TMA")

2. QUESTION STRUCTURE
   This is where you specify how your TMA is organised:

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

3. PACKAGE OPTIONS
   • roman: Use Roman numerals for part numbering (i, ii, iii). If not selected, alphabetic numbering (a, b, c) is used.
   • cleveref: Enable cleveref for smart cross-referencing.
   • pdfbookmark: Add PDF bookmarks for questions.
   • legacy: Enable legacy command definitions (e.g., \vec).

4. CONTROLS

   🔧 BUTTONS:
   • Add Question: Creates a new question entry
   • Clear All: Resets all fields and questions to their default values.
   • Example: Populates the form with example questions.
   • Generate TMA Files: Creates the LaTeX file structure
   • Save Settings: Saves your configuration for next time
   • Help: Shows this help dialog

5. USING WITH OVERLEAF

This tool generates files specifically for Overleaf:

1. CREATE OVERLEAF PROJECT:
   • Go to overleaf.com and sign in
   • Click "New Project" → "Blank Project"
   • Use the suggested project name from output
   • (e.g., "M101 TMA 04 (2026)")

2. UPLOAD GENERATED FILES:
   • Delete the default main.tex file in Overleaf
   • Upload ALL files from your output directory
   • This includes .tex files and .sty style files
   • Use drag & drop or the upload button

3. COMPILE AND EDIT:
   • Set TMA.tex as main document (if not automatic)
   • Click "Recompile" to generate PDF
   • Edit individual part files (q1a.tex, q1b.tex, etc.)
   • View formatted output in PDF preview

Overleaf provides automatic compilation, cloud storage, and professional formatting with the included style files. No local LaTeX installation required!
        """


class ConfigManager:
    """
    Handle loading and saving of application configuration.
    """
    
    @staticmethod
    def load_config() -> Dict[str, str]:
        try:
            if Path(CONFIG_FILE).exists():
                with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                    loaded_config = json.load(file)
                    config = DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
        except (json.JSONDecodeError, IOError) as error:
            print(f"Warning: Could not load config file: {error}")
        return DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: Dict[str, str]) -> bool:
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=2)
            return True
        except IOError as error:
            print(f"Warning: Could not save config file: {error}")
            return False


class LaTeXFileGenerator:
    """
    Generate LaTeX files from question structure.
    """
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
    
    def create_directory(self, directory: str) -> str:
        directory_path = Path(directory).resolve()
        try:
            directory_path.mkdir(parents=True, exist_ok=False)
            return str(directory_path)
        except FileExistsError:
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            backup_path = f"{directory_path}.{timestamp}"
            print(f'Directory {directory_path} exists, renaming to {backup_path}')
            os.rename(directory_path, backup_path)
            directory_path.mkdir(parents=True)
            return str(directory_path)
    
    def create_main_tex_file(self, folder: str, basename: str, number_of_questions: int) -> None:
        file_path = Path(folder) / f"{basename}{TEX_EXTENSION}"
        try:
            content = self._generate_main_tex_content(basename=basename, number_of_questions=number_of_questions)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except IOError as error:
            raise Exception(f"Error creating main LaTeX file: {error}")
    
    def _generate_main_tex_content(self, basename: str, number_of_questions: int) -> str:
        lines = [
            f"% File: {basename}.tex",
            "% This is the MAIN document file - DO NOT EDIT!",
            "% This file is auto-generated and controls the overall document structure.",
            "% To add your answers, edit the individual question part files (e.g., q1a.tex, q1b.tex)",
            "% Generated by TMA LaTeX Generator",
            "",
        ]
        if MAIN_TEX_PROGRAM:
            lines.append(MAIN_TEX_PROGRAM)
        lines.append("\\documentclass[a4paper,12pt]{article}")
        options = []
        if self.config.get("roman"):
            options.append("roman")
        else:
            options.append("alph")
        if self.config.get("cleveref"):
            options.append("cleveref")
        if self.config.get("pdfbookmark"):
            options.append("pdfbookmark")
        if self.config.get("legacy"):
            options.append("legacy")
        if options:
            style_package_line = f"\\usepackage[{','.join(options)}]{{{self.config['style']}}}"
        else:
            style_package_line = f"\\usepackage{{{self.config['style']}}}"
        lines.append(style_package_line)
        lines.append(f"\\myname{{{self.config['name']}}}")
        lines.append(f"\\mypin{{{self.config['pin']}}}")
        lines.append(f"\\mycourse{{{self.config['course']}}}")
        lines.append(f"\\mytma{{{self.config['tma_ref']}}}")
        lines.append(f"\\setdate{{{self.config['cod']}}}")
        lines.append("")
        include_files = [f"{QUESTION_PREFIX}{i+1}" for i in range(number_of_questions)]
        lines.append(f"\\includeonly{{{','.join(include_files)}}}")
        lines.append("")
        lines.append("\\begin{document}")
        for i in range(number_of_questions):
            lines.append(f"\\include{{{QUESTION_PREFIX}{i+1}}}")
        lines.append("\\end{document}")
        return '\n'.join(lines)
    
    def create_question_files(self, folder: str, basename: str, question_number: str, parts: Tuple[str, ...]) -> None:
        try:
            folder_path = Path(folder)
            question_content = self._generate_question_content(basename, question_number, parts)
            question_filename = folder_path / f"{QUESTION_PREFIX}{question_number}{TEX_EXTENSION}"
            with open(question_filename, 'w', encoding='utf-8') as file:
                file.write(question_content)
            for part in parts:
                part_filename = folder_path / f"{QUESTION_PREFIX}{question_number}{part}{TEX_EXTENSION}"
                part_content = [
                    f"% !TeX root = ./{basename}{TEX_EXTENSION}",
                    f"% File: {QUESTION_PREFIX}{question_number}{part}.tex",
                    "% This is an ANSWER file - EDIT THIS!",
                    f"% Add your answer for Question {question_number} part ({part}) below.",
                    "% You can use LaTeX commands, equations, figures, etc.",
                    "% Generated by TMA LaTeX Generator",
                    "",
                    "% Add your answer here:",
                    ""
                ]
                with open(part_filename, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(part_content))
        except IOError as error:
            raise Exception(f"Error creating question files: {error}")
    
    def _generate_question_content(self, basename: str, question_number: str, parts: Tuple[str, ...]) -> str:
        lines = [
            f"% !TeX root = ./{basename}{TEX_EXTENSION}",
            f"% File: q{question_number}.tex",
            "% This is a STRUCTURE file - DO NOT EDIT!",
            "% This file controls the layout of question parts.",
            f"% To add your answers, edit the individual part files (q{question_number}a.tex, q{question_number}b.tex, etc.)",
            "% Generated by TMA LaTeX Generator",
            ""
        ]
        lines.append("\\begin{question}")
        for part in parts:
            lines.append(f"\\qpart %({part})")
            lines.append(f"\\input{{{QUESTION_PREFIX}{question_number}{part}}}")
        lines.append("\\end{question}")
        return '\n'.join(lines)
    
    def create_subparts(self, folder: str, basename: str, subparts_dict: Dict[str, int]) -> None:
        try:
            folder_path = Path(folder)
            for part_id, num_subparts in subparts_dict.items():
                part_filename = folder_path / f"{part_id}{TEX_EXTENSION}"
                if part_filename.exists():
                    subpart_content = self._generate_subpart_content(basename, part_id, num_subparts)
                    with open(part_filename, 'a', encoding='utf-8') as file:
                        file.write(subpart_content)
                    for i in range(num_subparts):
                        subpart_filename = folder_path / f"{part_id}_{i}{TEX_EXTENSION}"
                        subpart_file_content = [
                            f"% !TeX root = ./{basename}{TEX_EXTENSION}",
                            f"% File: {part_id}_{i}.tex",
                            "% This is a SUBPART ANSWER file - EDIT THIS!",
                            f"% Add your answer for subpart {i+1} here.",
                            "% You can use LaTeX commands, equations, figures, etc.",
                            "% Generated by TMA LaTeX Generator",
                            "",
                            "% Add your answer here:",
                            ""
                        ]
                        with open(subpart_filename, 'w', encoding='utf-8') as file:
                            file.write('\n'.join(subpart_file_content))
        except IOError as error:
            raise Exception(f"Error creating subpart files: {error}")
    
    def _generate_subpart_content(self, basename: str, part_id: str, num_subparts: int ) -> str:
        lines = []
        for i in range(num_subparts):
            lines.append('\n\\qsubpart')
            lines.append(f'\\input{{{part_id}_{i}}}')
        return ''.join(lines)
    
    def copy_style_files(self, output_folder: str) -> List[str]:
        copied_files = []
        current_dir = Path.cwd()
        output_path = Path(output_folder)
        try:
            sty_file = current_dir / "ou-tma.sty"
            if sty_file.exists():
                dest_file = output_path / sty_file.name
                shutil.copy2(sty_file, dest_file)
                copied_files.append(sty_file.name)
        except (IOError, OSError) as error:
            raise Exception(f"Error copying style files: {error}")
        return copied_files


class TMAGeneratorGUI:
    """
    Main GUI application for TMA LaTeX Generator.
    """
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config = ConfigManager.load_config()
        self.questions: List[Dict[str, tk.StringVar]] = []
        self._setup_main_window()
        self._create_widgets()
    
    def _setup_main_window(self) -> None:
        self.root.title("TMA LaTeX Generator")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _create_widgets(self) -> None:
        main_frame = ttk.Frame(self.root, padding=MAIN_FRAME_PADDING)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        row = 0
        row = self._create_title_section(main_frame, row)
        row = self._create_basic_settings_section(main_frame, row)
        row = self._create_question_structure_section(main_frame, row)
        row = self._create_action_buttons_section(main_frame, row)
        self._create_output_section(main_frame, row)
    
    def _create_title_section(self, parent: ttk.Frame, row: int) -> int:
        title_label = ttk.Label(parent, text="TMA LaTeX Generator", font=("Arial", 16, "bold"))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 10))
        row += 1
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, SEPARATOR_PADY))
        row += 1
        return row
    
    def _create_basic_settings_section(self, parent: ttk.Frame, row: int) -> int:
        settings_fields = [
            ("Course Code:", "course", 15, "Your module code (e.g., MATH101, PHYS201, CHEM301)", True),
            ("TMA Reference:", "tma_ref", 10, "TMA assignment number (e.g., 01, 02, 03, 04)", True),
            ("Date:", "cod", 20, "This is a free format field, any rendition of 'data' may be given e.g. '21 October 2025'. You may retrieve this date later using the '\\thedate' command.", True),
            ("Title:", "title", 30, "Optional title for the TMA, which will appear on the title page", True),
            ("Your Name:", "name", 30, "Your full name as registered with your institution", True),
            ("Student PIN:", "pin", 15, "Your student identification number (e.g., S1234567)", True),
            ("LaTeX Style:", "style", 10, "Obtained from:https://ctan.org/pkg/ou-tma", False),
        ]
        for label_text, config_key, width, tooltip_text, editable in settings_fields:
            row = self._create_labeled_entry(parent, row, label_text, config_key, width, tooltip_text, editable)
        options_frame = ttk.LabelFrame(parent, text="Package Options")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        self.roman_var = tk.BooleanVar(value=self.config.get("roman", False))
        self.cleveref_var = tk.BooleanVar(value=self.config.get("cleveref", False))
        self.pdfbookmark_var = tk.BooleanVar(value=self.config.get("pdfbookmark", False))
        self.legacy_var = tk.BooleanVar(value=self.config.get("legacy", False))
        options = [
            ("roman", self.roman_var, "Use Roman numerals for part numbering (i, ii, iii)"),
            ("cleveref", self.cleveref_var, "Enable cleveref for smart cross-referencing"),
            ("pdfbookmark", self.pdfbookmark_var, "Add PDF bookmarks for questions"),
            ("legacy", self.legacy_var, "Enable legacy command definitions (e.g., \\vec)")
        ]
        for i, (text, var, tooltip) in enumerate(options):
            cb = ttk.Checkbutton(options_frame, text=text, variable=var)
            cb.grid(row=0, column=i, sticky=tk.W, padx=5, pady=2)
            ToolTip(cb, tooltip)
        self.roman_var.trace_add('write', self._on_roman_toggle)
        row = self._create_output_directory_field(parent, row)
        row = self._create_labeled_entry(
            parent, row, "Base Filename:", "basename", 15,
            "Name for main LaTeX file (usually 'TMA'). Creates TMA.tex as main file."
        )
        return row
    
    def _create_labeled_entry(self, parent: ttk.Frame, row: int, label_text: str, config_key: str, width: int, tooltip_text: str, editable: bool = True) -> int:
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=ENTRY_PADY)
        var = tk.StringVar(value=self.config[config_key])
        entry = ttk.Entry(parent, textvariable=var, width=width)
        if not editable:
            entry.config(state='readonly')
        entry.grid(row=row, column=1, sticky=tk.W, pady=ENTRY_PADY, padx=(5, 0))
        setattr(self, f"{config_key}_var", var)
        ToolTip(entry, tooltip_text)
        return row + 1
    
    def _create_output_directory_field(self, parent: ttk.Frame, row: int) -> int:
        ttk.Label(parent, text="Output Directory:").grid(row=row, column=0, sticky=tk.W, pady=ENTRY_PADY)
        self.output_var = tk.StringVar(value=self.config["output"])
        output_entry = ttk.Entry(parent, textvariable=self.output_var, width=30)
        output_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=ENTRY_PADY, padx=(5, 0))
        ToolTip(output_entry, "Directory where LaTeX files will be created. Use Browse button or type path directly.")
        browse_button = ttk.Button(parent, text="Browse", command=self._browse_output)
        browse_button.grid(row=row, column=2, pady=ENTRY_PADY, padx=(5, 0))
        ToolTip(browse_button, "Click to select output directory")
        return row + 1
    
    def _create_question_structure_section(self, parent: ttk.Frame, row: int) -> int:
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=SEPARATOR_PADY)
        row += 1
        structure_label = ttk.Label(parent, text="Question Structure (Manual Input)", font=("Arial", 12, "bold"))
        structure_label.grid(row=row, column=0, columnspan=3, pady=(0, 5))
        row += 1
        row = self._create_structure_control_buttons(parent, row)
        row = self._create_scrollable_question_area(parent, row)
        return row
    
    def _create_structure_control_buttons(self, parent: ttk.Frame, row: int) -> int:
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=3, pady=5)
        buttons = [
            ("Clear All", self._clear_structure, "Resets all fields and questions to their default values."),
            ("Add Question", self._add_question, "Add a new question to the structure"),
            ("Example", self._add_example_questions, "Populate with example questions that demonstrate the functionality"),
            ("Help", self._show_help, "Show comprehensive help with examples and instructions"),
        ]
        for text, command, tooltip in buttons:
            button = ttk.Button(control_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=BUTTON_PADX)
            ToolTip(button, tooltip)
        return row + 1
    
    def _create_scrollable_question_area(self, parent: ttk.Frame, row: int) -> int:
        self.structure_canvas = tk.Canvas(parent, height=200)
        self.structure_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.structure_canvas.yview)
        self.structure_scrollable_frame = ttk.Frame(self.structure_canvas)
        self.structure_scrollable_frame.bind("<Configure>", lambda e: self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all")))
        self.structure_canvas.create_window((0, 0), window=self.structure_scrollable_frame, anchor="nw")
        self.structure_canvas.configure(yscrollcommand=self.structure_scrollbar.set)
        self.structure_canvas.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        self.structure_scrollbar.grid(row=row, column=2, sticky=(tk.N, tk.S), pady=(5, 0))
        self._add_question()
        return row + 1
    
    def _create_action_buttons_section(self, parent: ttk.Frame, row: int) -> int:
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=SEPARATOR_PADY)
        row += 1
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        buttons = [
            ("Generate TMA Files", self._generate_files, "Create the LaTeX file structure based on your question setup"),
            ("Save Settings", self._save_settings, "Save your current configuration to avoid re-entering next time"),
            ("Exit", self.root.quit, "Close the application"),
        ]
        for text, command, tooltip in buttons:
            button = ttk.Button(button_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=BUTTON_PADX)
            ToolTip(button, tooltip)
        return row + 1
    
    def _create_output_section(self, parent: ttk.Frame, row: int) -> None:
        ttk.Label(parent, text="Output:").grid(row=row, column=0, sticky=tk.W, pady=(10, 0))
        row += 1
        self.output_text = scrolledtext.ScrolledText(parent, width=70, height=15)
        self.output_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 10))
        parent.rowconfigure(row, weight=1)
    
    def _browse_output(self) -> None:
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
    
    def _show_help(self) -> None:
        HelpDialog(self.root)

    def _add_example_questions(self) -> None:
        if self.questions:
            if not messagebox.askyesno("Add Example Questions", "This will clear all current questions. Are you sure?"):
                return
        self.questions = []
        use_roman = self.roman_var.get()
        if use_roman:
            self.course_var.set('M381')
            example_questions = [
                {'marks': '25', 'parts': 'i,ii', 'subparts': 'i:a,b;ii:a,b,c'},
                {'marks': '25', 'parts': 'i,ii,iii', 'subparts': 'i:a,b'},
                {'marks': '30', 'parts': 'i,ii,iii,iv', 'subparts': 'iv:a,b,c,d'},
                {'marks': '20', 'parts': 'i', 'subparts': ''}
            ]
        else:
            example_questions = [
                {'marks': '25', 'parts': 'a,b', 'subparts': 'a:i,ii;b:i,ii,iii'},
                {'marks': '25', 'parts': 'a,b,c', 'subparts': 'a:i,ii'},
                {'marks': '30', 'parts': 'a,b,c,d', 'subparts': 'd:i,ii,iii,iv'},
                {'marks': '20', 'parts': 'a', 'subparts': ''}
            ]
        for q_data in example_questions:
            new_question = {
                'marks_var': tk.StringVar(value=q_data['marks']),
                'parts_var': tk.StringVar(value=q_data['parts']),
                'subparts_var': tk.StringVar(value=q_data['subparts']),
            }
            self.questions.append(new_question)
        self._refresh_question_frames()
    
    def _save_settings(self) -> None:
        config = self._get_current_config()
        if ConfigManager.save_config(config):
            self.config = config
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
        else:
            messagebox.showerror("Error", "Could not save settings to file.")
    
    def _get_current_config(self) -> Dict[str, str]:
        return {
            "course": self.course_var.get(),
            "tma_ref": self.tma_ref_var.get(),
            "cod": self.cod_var.get(),
            "name": self.name_var.get(),
            "pin": self.pin_var.get(),
            "style": self.style_var.get(),
            "output": self.output_var.get(),
            "basename": self.basename_var.get(),
            "roman": self.roman_var.get(),
            "cleveref": self.cleveref_var.get(),
            "pdfbookmark": self.pdfbookmark_var.get(),
            "legacy": self.legacy_var.get()
        }

    def _on_roman_toggle(self, *args):
        """Handle toggling of the 'roman' checkbox to convert parts and subparts."""
        is_roman = self.roman_var.get()
        alph_map = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        roman_map = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii']
        part_from_map = alph_map if is_roman else roman_map
        part_to_map = roman_map if is_roman else alph_map
        subpart_from_map = roman_map if is_roman else alph_map
        subpart_to_map = alph_map if is_roman else roman_map
        for question in self.questions:
            current_parts_str = question['parts_var'].get()
            current_parts = [p.strip() for p in current_parts_str.split(',') if p.strip()]
            new_parts = []
            for part in current_parts:
                try:
                    index = part_from_map.index(part)
                    new_parts.append(part_to_map[index])
                except ValueError:
                    new_parts.append(part)
            question['parts_var'].set(','.join(new_parts))
            current_subparts_str = question['subparts_var'].get()
            if current_subparts_str.strip():
                subpart_groups = [s.strip() for s in current_subparts_str.split(';') if s.strip()]
                new_subpart_groups = []
                for group in subpart_groups:
                    if ':' not in group:
                        new_subpart_groups.append(group)
                        continue
                    part_key, sub_values_str = group.split(':', 1)
                    part_key = part_key.strip()
                    try:
                        key_index = part_from_map.index(part_key)
                        new_part_key = part_to_map[key_index]
                    except ValueError:
                        new_part_key = part_key
                    sub_values = [s.strip() for s in sub_values_str.split(',') if s.strip()]
                    new_sub_values = []
                    for val in sub_values:
                        try:
                            val_index = subpart_from_map.index(val)
                            new_sub_values.append(subpart_to_map[val_index])
                        except ValueError:
                            new_sub_values.append(val)
                    new_subpart_groups.append(f"{new_part_key}:{','.join(new_sub_values)}")
                question['subparts_var'].set('; '.join(new_subpart_groups))

    def _add_question(self) -> None:
        self._insert_question(len(self.questions))

    def _insert_question(self, index: int) -> None:
        default_parts = 'i,ii,iii,iv' if self.roman_var.get() else 'a,b,c,d'
        new_question = {
            'marks_var': tk.StringVar(value='25'),
            'parts_var': tk.StringVar(value=default_parts),
            'subparts_var': tk.StringVar(value=''),
        }
        self.questions.insert(index, new_question)
        self._refresh_question_frames()

    def _remove_question(self, index: int) -> None:
        question_text = f"Question {index + 1}"
        if not messagebox.askyesno("Remove Question", f"Remove {question_text}? This cannot be undone."):
            return
        del self.questions[index]
        if not self.questions:
            self._add_question()
        else:
            self._refresh_question_frames()

    def _refresh_question_frames(self) -> None:
        for widget in self.structure_scrollable_frame.winfo_children():
            widget.destroy()
        for i, question_data in enumerate(self.questions):
            question_num = i + 1
            question_frame = ttk.LabelFrame(self.structure_scrollable_frame, text=f"Question {question_num}")
            question_frame.pack(fill=tk.X, padx=5, pady=2)
            details_frame = ttk.Frame(question_frame)
            details_frame.pack(fill=tk.X, padx=5, pady=2)
            self._create_question_input_fields(details_frame, i, question_data)
        self._update_scroll_region()

    def _create_question_input_fields(self, parent: ttk.Frame, index: int, question_data: Dict[str, tk.StringVar]) -> None:
        field_defs = [
            ("Marks:", question_data['marks_var'], 5, "Total marks for this question (e.g., 25, 30, 15)"),
            ("Parts:", question_data['parts_var'], 20, "Question parts separated by commas\nExamples: 'a,b,c,d' or 'a,b' or 'a,b,c,d,e,f'"),
            ("Subparts (part:subparts):", question_data['subparts_var'], 15, "Subparts for each part using format: part:sub1,sub2\nExamples:\n'a:i,ii,iii' or 'a:a,b,c'\nLeave blank if no subparts"),
        ]
        for label_text, var, width, tooltip in field_defs:
            ttk.Label(parent, text=label_text).pack(side=tk.LEFT)
            entry = ttk.Entry(parent, textvariable=var, width=width)
            entry.pack(side=tk.LEFT, padx=(2, 10))
            ToolTip(entry, tooltip)
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.RIGHT)
        add_button = ttk.Button(button_frame, text="Add", command=lambda i=index: self._insert_question(i + 1))
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        ToolTip(add_button, "Insert a new question after this one")
        remove_button = ttk.Button(button_frame, text="Remove", command=lambda i=index: self._remove_question(i))
        remove_button.pack(side=tk.LEFT)
        ToolTip(remove_button, "Remove this question from the structure")

    def _clear_structure(self) -> None:
        self.course_var.set(DEFAULT_CONFIG["course"])
        self.tma_ref_var.set(DEFAULT_CONFIG["tma_ref"])
        self.cod_var.set(DEFAULT_CONFIG["cod"])
        self.title_var.set(DEFAULT_CONFIG["title"])
        self.name_var.set(DEFAULT_CONFIG["name"])
        self.pin_var.set(DEFAULT_CONFIG["pin"])
        self.style_var.set(DEFAULT_CONFIG["style"])
        self.basename_var.set(DEFAULT_CONFIG["basename"])
        self.output_var.set(DEFAULT_CONFIG["output"])
        self.roman_var.set(False)
        self.cleveref_var.set(False)
        self.pdfbookmark_var.set(False)
        self.legacy_var.set(False)
        self.questions = []
        self._add_question()
        messagebox.showinfo("Clear", "All fields have been reset to their default values.")
    
    def _update_scroll_region(self) -> None:
        self.structure_canvas.update_idletasks()
        self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all"))
    
    def _get_manual_structure(self) -> Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]:
        structure = {}
        for i, question_data in enumerate(self.questions):
            q_id = f"Q{i + 1}"
            try:
                marks = int(question_data['marks_var'].get() or 25)
            except ValueError:
                marks = 25
            parts_text = question_data['parts_var'].get().strip()
            parts = [p.strip() for p in parts_text.split(',') if p.strip()]
            subparts_dict = self._parse_subparts_string(question_data['subparts_var'].get().strip())
            structure[q_id] = {'marks': marks, 'parts': {}}
            for part in parts:
                structure[q_id]['parts'][part] = {'subparts': subparts_dict.get(part, {})}
        return structure
    
    def _parse_subparts_string(self, subparts_text: str) -> Dict[str, Dict[str, bool]]:
        subparts_dict = {}
        if not subparts_text:
            return subparts_dict
        for part_subparts in subparts_text.split(';'):
            if ':' not in part_subparts:
                continue
            part, subparts_str = part_subparts.split(':', 1)
            part = part.strip()
            subparts = [s.strip() for s in subparts_str.split(',') if s.strip()]
            subparts_dict[part] = {s: True for s in subparts}
        return subparts_dict
    
    def _validate_question_structure(self) -> Optional[str]:
        total_marks = 0
        for i, question_data in enumerate(self.questions):
            question_num = i + 1
            marks_text = question_data['marks_var'].get().strip()
            try:
                marks = int(marks_text) if marks_text else 25
                if marks <= 0:
                    return f"Question {question_num}: Marks must be a positive number (got '{marks_text}')."
                total_marks += marks
            except ValueError:
                return f"Question {question_num}: Marks must be a valid number (got '{marks_text}')."
            parts_text = question_data['parts_var'].get().strip()
            parts = [p.strip().lower() for p in parts_text.split(',') if p.strip()]
            if not parts:
                return f"Question {question_num}: No parts specified. Please add at least one part (e.g., 'a,b,c,d')."
            if len(parts) != len(set(parts)):
                duplicates = [p for p in set(parts) if parts.count(p) > 1]
                return f"Question {question_num}: Duplicate parts found: {', '.join(duplicates)}. Each part should be unique."
            subparts_text = question_data['subparts_var'].get().strip()
            if not subparts_text:
                continue
            subparts_dict = self._parse_subparts_string(subparts_text)
            for subpart_part in subparts_dict.keys():
                subpart_part_lower = subpart_part.strip().lower()
                if subpart_part_lower not in parts:
                    available_parts = ', '.join(parts)
                    return (f"Question {question_num}: Subpart references part '{subpart_part}' which doesn't exist.\n"
                           f"Available parts: {available_parts}\n"
                           f"Check your subparts format: 'part:sub1,sub2;part2:sub1,sub2'")
            for part, subpart_dict in subparts_dict.items():
                if not subpart_dict:
                    return f"Question {question_num}: Part '{part}' has no subparts specified. Either remove '{part}:' or add subparts like '{part}:i,ii,iii'."
        if total_marks != 100:
            return self._handle_marks_total_mismatch(total_marks)
        return None
    
    def _handle_marks_total_mismatch(self, total_marks: int) -> Optional[str]:
        num_questions = len(self.questions)
        if total_marks < 100:
            message = (f"Total marks: {total_marks} (should be 100)\n\n"
                      f"You currently have {num_questions} question(s).\n"
                      f"The marks are {100 - total_marks} short of 100.\n\n"
                      f"Possible issues:\n"
                      f"• Too few questions - consider adding more questions\n"
                      f"• Question marks are too low - consider increasing marks per question\n\n"
                      f"Do you want to continue generating files anyway?")
        else:
            message = (f"Total marks: {total_marks} (should be 100)\n\n"
                      f"You currently have {num_questions} question(s).\n"
                      f"The marks are {total_marks - 100} over 100.\n\n"
                      f"Possible issues:\n"
                      f"• Too many questions - consider removing some questions\n"
                      f"• Question marks are too high - consider reducing marks per question\n\n"
                      f"Do you want to continue generating files anyway?")
        continue_anyway = messagebox.askyesno("Marks Total Warning", message, icon='warning')
        if continue_anyway:
            return None
        else:
            return f"File generation cancelled. Please adjust your questions so the total marks equal 100 (currently: {total_marks})."
    
    def _generate_files(self) -> None:
        self.output_text.delete(1.0, tk.END)
        if not self.questions:
            messagebox.showerror("Error", "Please add at least one question.")
            return
        try:
            config = self._get_current_config()
            validation_error = self._validate_question_structure()
            if validation_error:
                messagebox.showerror("Validation Error", validation_error)
                return
            structure = self._get_manual_structure()
            success, message = self._generate_tма_files(config, structure)
            if success:
                self.config = config
                ConfigManager.save_config(self.config)
                messagebox.showinfo("Success", "TMA files generated successfully!")
            else:
                messagebox.showerror("Error", message)
        except Exception as error:
            error_msg = f"Unexpected error: {str(error)}"
            self.output_text.insert(tk.END, f"{error_msg}\n")
            messagebox.showerror("Error", error_msg)
    
    def _generate_tma_files(self, config: Dict[str, str], structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]) -> Tuple[bool, str]:
        try:
            generator = LaTeXFileGenerator(config)
            self.output_text.insert(tk.END, "Using manual question structure...\n")
            self.output_text.see(tk.END)
            self.output_text.update()
            self._display_structure_summary(structure)
            parts_list, subparts_dict = self._prepare_generation_data(structure)
            actual_folder = generator.create_directory(config["output"])
            self.output_text.insert(tk.END, f"Created directory: {actual_folder}\n")
            self.output_text.see(tk.END)
            self.output_text.update()
            generator.create_main_tex_file(actual_folder, config["basename"], len(structure))
            for i, question_parts in enumerate(parts_list):
                generator.create_question_files(actual_folder, config["basename"], str(i + 1), question_parts)
            if subparts_dict:
                generator.create_subparts(actual_folder, config["basename"], subparts_dict)
            copied_styles = generator.copy_style_files(actual_folder)
            if copied_styles:
                self.output_text.insert(tk.END, f"Copied style files: {', '.join(copied_styles)}\n")
                self.output_text.see(tk.END)
                self.output_text.update()
            suggested_name = self._generate_overleaf_project_name(config)
            success_message = f"TMA files successfully created in {actual_folder}"
            self.output_text.insert(tk.END, f"{success_message}\n")
            self.output_text.insert(tk.END, "\n=== OVERLEAF SETUP ===\n")
            self.output_text.insert(tk.END, f"Suggested Overleaf project name:\n")
            self.output_text.insert(tk.END, f"  {suggested_name}\n\n")
            self.output_text.insert(tk.END, "Next steps:\n")
            self.output_text.insert(tk.END, "1. Create new blank project in Overleaf\n")
            self.output_text.insert(tk.END, "2. Use the suggested name above\n")
            self.output_text.insert(tk.END, "3. Delete default main.tex in Overleaf\n")
            self.output_text.insert(tk.END, "4. Upload ALL files from output directory\n")
            self.output_text.insert(tk.END, "5. Compile and start editing!\n\n")
            self.output_text.insert(tk.END, "Generation completed successfully!\n")
            self.output_text.see(tk.END)
            return True, success_message
        except Exception as error:
            error_message = f"Error: {str(error)}"
            self.output_text.insert(tk.END, f"{error_message}\n")
            self.output_text.see(tk.END)
            return False, error_message
    
    def _display_structure_summary(self, structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]) -> None:
        self.output_text.insert(tk.END, "Question Structure:\n")
        for q_id, q_data in sorted(structure.items(), key=lambda x: int(x[0][1:])):
            marks = q_data.get('marks', 'N/A')
            self.output_text.insert(tk.END, f"{q_id}: {marks} marks\n")
            for part_id in sorted(q_data.get('parts', {}).keys()):
                self.output_text.insert(tk.END, f"  ({part_id})\n")
                subparts = q_data['parts'][part_id].get('subparts', {})
                for subpart_id in sorted(subparts.keys()):
                    self.output_text.insert(tk.END, f"    ({subpart_id})\n")
        self.output_text.see(tk.END)
        self.output_text.update()
    
    def _prepare_generation_data(self, structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]) -> Tuple[List[Tuple[str, ...]], Dict[str, int]]:
        parts_list = []
        subparts_dict = {}
        for q_id in sorted(structure.keys(), key=lambda x: int(x[1:])):
            q_data = structure[q_id]
            question_parts = tuple(sorted(q_data.get('parts', {}).keys()))
            parts_list.append(question_parts)
            for part_id, part_data in q_data.get('parts', {}).items():
                subparts = list(part_data.get('subparts', {}).keys())
                if subparts:
                    subparts_dict[f"{QUESTION_PREFIX}{q_id[1:]}{part_id}"] = len(subparts)
        return parts_list, subparts_dict
    
    def _generate_overleaf_project_name(self, config: Dict[str, str]) -> str:
        course = config.get('course', 'COURSE').upper()
        tma_ref = config.get('tma_ref', '01').zfill(2)
        cod = config.get('cod', '').strip()
        year_suffix = ""
        if cod:
            import re
            year_match = re.search(r'\b(20\d{2})\b', cod)
            if year_match:
                year_suffix = f" ({year_match.group(1)})"
        project_name = f"{course} TMA {tma_ref}{year_suffix}"
        return project_name

def main() -> None:
    """Main function - GUI only since PDF processing has been removed."""
    try:
        root = tk.Tk()
        app = TMAGeneratorGUI(root)
        root.mainloop()
    except Exception as error:
        print(f"GUI Error: {error}")
        print("Error starting GUI. Please check tkinter installation.")


if __name__ == "__main__":
    main()