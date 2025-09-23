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
    "name": "Alex Taylor",
    "pin": "S1234567",
    "style": "tma",
    "output": "./output",
    "basename": "TMA"
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
        """
        Initialize tooltip for a widget.
        
        Args:
            widget: The tkinter widget to attach tooltip to
            text: The tooltip text to display
        """
        self.widget = widget
        self.text = text
        self.tooltip_window: Optional[tk.Toplevel] = None
        
        # Bind mouse events to show/hide tooltip
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event: Optional[tk.Event] = None) -> None:
        """
        Show tooltip when mouse enters widget.
        
        Args:
            event: Tkinter event object (unused)
        """
        if not self.text:
            return
            
        try:
            # Get widget position for tooltip placement
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
        except tk.TclError:
            # Widget doesn't support bbox, use alternative positioning
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip_window = tooltip = tk.Toplevel(self.widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create and pack tooltip label
        label = tk.Label(
            tooltip,
            text=self.text,
            justify='left',
            **TOOLTIP_STYLE
        )
        label.pack(ipadx=5, ipady=3)
    
    def on_leave(self, event: Optional[tk.Event] = None) -> None:
        """
        Hide tooltip when mouse leaves widget.
        
        Args:
            event: Tkinter event object (unused)
        """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def update_text(self, new_text: str) -> None:
        """
        Update tooltip text.
        
        Args:
            new_text: New text to display in tooltip
        """
        self.text = new_text


class HelpDialog:
    """
    Comprehensive help dialog with usage instructions and examples.
    
    Displays a modal dialog containing detailed information about how to use
    the TMA LaTeX Generator, including examples and troubleshooting tips.
    """
    
    def __init__(self, parent: tk.Widget) -> None:
        """
        Initialize and display help dialog.
        
        Args:
            parent: Parent widget for modal dialog
        """
        self.dialog = tk.Toplevel(parent)
        self._setup_dialog(parent)
        self._create_help_content()
        self._center_dialog()
    
    def _setup_dialog(self, parent: tk.Widget) -> None:
        """
        Configure dialog window properties.
        
        Args:
            parent: Parent widget for modal dialog
        """
        self.dialog.title("TMA LaTeX Generator - Help")
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
    
    def _center_dialog(self) -> None:
        """Centre dialogue on screen."""
        self.dialog.update_idletasks()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        dialogue_width = self.dialog.winfo_width()
        dialogue_height = self.dialog.winfo_height()
        
        x = (screen_width // 2) - (dialogue_width // 2)
        y = (screen_height // 2) - (dialogue_height // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_help_content(self) -> None:
        """Create and populate help dialog content."""
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=MAIN_FRAME_PADDING)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="TMA LaTeX Generator - User Guide",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Scrolled text widget for content
        text_widget = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            height=30
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Insert help content
        help_content = self._get_help_content()
        text_widget.insert(tk.END, help_content)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        close_button = ttk.Button(
            main_frame,
            text="Close",
            command=self.dialog.destroy
        )
        close_button.pack(pady=(5, 0))
    
    def _get_help_content(self) -> str:
        """
        Generate comprehensive help content.
        
        Returns:
            Formatted help text with examples and instructions
        """
        return """🎯 OVERVIEW

The TMA LaTeX Generator creates structured LaTeX files for academic assignments, specifically designed for Overleaf. You manually specify the question structure, and the application generates all necessary files organised for easy editing and upload to Overleaf.

📋 STEP-BY-STEP GUIDE

1. BASIC SETTINGS
   • Course Code: Your module code (e.g., MATH101, PHYS201, etc.)
   • TMA Reference: Assignment number (e.g., 01, 02, 03, 04)
   • Cut-off Date: Submission deadline (e.g., "21 January 2026")
   • Your Name: Your full name as registered
   • Student PIN: Your student identification number
   • LaTeX Style: Style file to use (usually "tma")
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

   🏫 TYPICAL ACADEMIC TMA STRUCTURE:
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

📞 USING WITH OVERLEAF

This tool generates files specifically for Overleaf:

1. CREATE OVERLEAF PROJECT:
   • Go to overleaf.com and sign in
   • Click "New Project" → "Blank Project"
   • Use the suggested project name from output
   • (e.g., "MATH101 TMA 04 (2026)")

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
    
    Manages persistent storage of user preferences and settings
    using JSON format configuration file.
    """
    
    @staticmethod
    def load_config() -> Dict[str, str]:
        """
        Load configuration from file.
        
        Returns:
            Dictionary containing configuration values, defaults if file not found
        """
        try:
            if Path(CONFIG_FILE).exists():
                with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                    loaded_config = json.load(file)
                    # Merge with defaults to ensure all keys exist
                    config = DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
        except (json.JSONDecodeError, IOError) as error:
            print(f"Warning: Could not load config file: {error}")
        
        return DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: Dict[str, str]) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
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
    
    Handles creation of main LaTeX document and all associated
    question, part, and subpart files.
    """
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize generator with configuration.
        
        Args:
            config: Configuration dictionary with file generation settings
        """
        self.config = config
    
    def create_directory(self, directory: str) -> str:
        """
        Create output directory, handling existing directories.
        
        Args:
            directory: Path to directory to create
            
        Returns:
            Actual directory path (may be renamed if original exists)
            
        Raises:
            Exception: If directory creation fails
        """
        directory_path = Path(directory).resolve()
        
        try:
            directory_path.mkdir(parents=True, exist_ok=False)
            return str(directory_path)
        except FileExistsError:
            # Create timestamped backup name if directory exists
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            backup_path = f"{directory_path}.{timestamp}"
            
            print(f'Directory {directory_path} exists, renaming to {backup_path}')
            os.rename(directory_path, backup_path)
            
            # Create new directory
            directory_path.mkdir(parents=True)
            return str(directory_path)
    
    def create_main_tex_file(
        self,
        folder: str,
        basename: str,
        number_of_questions: int
    ) -> None:
        """
        Create the main LaTeX document file.
        
        Args:
            folder: Output directory path
            basename: Base filename for main document
            number_of_questions: Total number of questions to include
            
        Raises:
            Exception: If file creation fails
        """
        file_path = Path(folder) / f"{basename}{TEX_EXTENSION}"
        
        try:
            content = self._generate_main_tex_content(
                basename=basename,
                number_of_questions=number_of_questions
            )
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
        except IOError as error:
            raise Exception(f"Error creating main LaTeX file: {error}")
    
    def _generate_main_tex_content(
        self,
        basename: str,
        number_of_questions: int
    ) -> str:
        """
        Generate content for main LaTeX document.
        
        Args:
            basename: Base filename
            number_of_questions: Number of questions to include
            
        Returns:
            Complete LaTeX document content as string
        """
        lines = []
        
        # Add header comment
        lines.append(f"% File: {basename}.tex")
        lines.append("% This is the MAIN document file - DO NOT EDIT!")
        lines.append("% This file is auto-generated and controls the overall document structure.")
        lines.append("% To add your answers, edit the individual question part files (e.g., q1a.tex, q1b.tex)")
        lines.append("% Generated by TMA LaTeX Generator")
        lines.append("")
        
        if MAIN_TEX_PROGRAM:
            lines.append(MAIN_TEX_PROGRAM)
        lines.append("\\documentclass[a4paper,12pt]{article}")
        lines.append(f"\\usepackage{{{self.config['style']}}}")
        lines.append(f"\\myname{{{self.config['name']}}}")
        lines.append(f"\\mypin{{{self.config['pin']}}}")
        lines.append(f"\\mycourse{{{self.config['course']}}}")
        lines.append(f"\\mytma{{{self.config['tma_ref']}}}")
        lines.append(f"\\mycod{{{self.config['cod']}}}")
        lines.append("")
        
        # Generate includeonly directive
        include_files = [f"{QUESTION_PREFIX}{i+1}" for i in range(number_of_questions)]
        lines.append(f"\\includeonly{{{','.join(include_files)}}}")
        lines.append("")
        
        # Generate document body
        lines.append("\\begin{document}")
        for i in range(number_of_questions):
            lines.append(f"\\t\\include{{{QUESTION_PREFIX}{i+1}}}")
        lines.append("\\end{document}")
        
        return '\n'.join(lines)
    
    def create_question_files(
        self,
        folder: str,
        basename: str,
        question_number: str,
        parts: Tuple[str, ...]
    ) -> None:
        """
        Create LaTeX files for a question and its parts.
        
        Args:
            folder: Output directory path
            basename: Base filename for references
            question_number: Question number as string
            parts: Tuple of part identifiers (e.g., ('a', 'b', 'c'))
            
        Raises:
            Exception: If file creation fails
        """
        try:
            folder_path = Path(folder)
            
            # Generate question file content
            question_content = self._generate_question_content(
                basename, question_number, parts
            )
            
            # Write main question file
            question_filename = folder_path / f"{QUESTION_PREFIX}{question_number}{TEX_EXTENSION}"
            with open(question_filename, 'w', encoding='utf-8') as file:
                file.write(question_content)
            
            # Create part files
            for part in parts:
                part_filename = folder_path / f"{QUESTION_PREFIX}{question_number}{part}{TEX_EXTENSION}"
                part_content = [
                    f"% File: {QUESTION_PREFIX}{question_number}{part}.tex",
                    "% This is an ANSWER file - EDIT THIS!",
                    f"% Add your answer for Question {question_number} part ({part}) below.",
                    "% You can use LaTeX commands, equations, figures, etc.",
                    "% Generated by TMA LaTeX Generator",
                    "",
                    f"% !TeX root = ./{basename}{TEX_EXTENSION}",
                    "",
                    "% Add your answer here:",
                    ""
                ]
                
                with open(part_filename, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(part_content))
                    
        except IOError as error:
            raise Exception(f"Error creating question files: {error}")
    
    def _generate_question_content(
        self,
        basename: str,
        question_number: str,
        parts: Tuple[str, ...]
    ) -> str:
        """
        Generate content for question LaTeX file.
        
        Args:
            basename: Base filename for root reference
            question_number: Question number
            parts: Part identifiers
            
        Returns:
            Question file content as string
        """
        lines = [
            f"% File: q{question_number}.tex",
            "% This is a STRUCTURE file - DO NOT EDIT!",
            "% This file controls the layout of question parts.",
            f"% To add your answers, edit the individual part files (q{question_number}a.tex, q{question_number}b.tex, etc.)",
            "% Generated by TMA LaTeX Generator",
            "",
            f"% !TeX root = ./{basename}{TEX_EXTENSION}"
        ]
        lines.append("\\begin{question}")
        
        for part in parts:
            part_letter = chr(97 + ord(part) - ord('a'))  # Ensure lowercase
            lines.append(f"\\t\\qpart %({part_letter})")
            lines.append(f"\\t\\input{{{QUESTION_PREFIX}{question_number}{part}}}")
        
        lines.append("\\end{question}")
        return '\n'.join(lines)
    
    def create_subparts(
        self,
        folder: str,
        basename: str,
        subparts_dict: Dict[str, int]
    ) -> None:
        """
        Create subpart files for questions.
        
        Args:
            folder: Output directory path  
            basename: Base filename for references
            subparts_dict: Dictionary mapping part IDs to subpart count
            
        Raises:
            Exception: If file creation fails
        """
        try:
            folder_path = Path(folder)
            
            for part_id, num_subparts in subparts_dict.items():
                part_filename = folder_path / f"{part_id}{TEX_EXTENSION}"
                
                if part_filename.exists():
                    # Append subpart structure to existing part file
                    subpart_content = self._generate_subpart_content(
                        basename, part_id, num_subparts
                    )
                    
                    with open(part_filename, 'a', encoding='utf-8') as file:
                        file.write(subpart_content)
                    
                    # Create individual subpart files
                    for i in range(num_subparts):
                        subpart_filename = folder_path / f"{part_id}_{i}{TEX_EXTENSION}"
                        subpart_file_content = [
                            f"% File: {part_id}_{i}.tex",
                            "% This is a SUBPART ANSWER file - EDIT THIS!",
                            f"% Add your answer for subpart {i+1} here.",
                            "% You can use LaTeX commands, equations, figures, etc.",
                            "% Generated by TMA LaTeX Generator",
                            "",
                            f"% !TeX root = ./{basename}{TEX_EXTENSION}",
                            "",
                            "% Add your answer here:",
                            ""
                        ]
                        
                        with open(subpart_filename, 'w', encoding='utf-8') as file:
                            file.write('\n'.join(subpart_file_content))
                            
        except IOError as error:
            raise Exception(f"Error creating subpart files: {error}")
    
    def _generate_subpart_content(
        self,
        basename: str,
        part_id: str,
        num_subparts: int
    ) -> str:
        """
        Generate subpart structure content.
        
        Args:
            basename: Base filename
            part_id: Part identifier
            num_subparts: Number of subparts to create
            
        Returns:
            Subpart structure as string
        """
        lines = []
        for i in range(num_subparts):
            lines.append('\n\\qsubpart')
            lines.append(f'\\input{{{part_id}_{i}}}')
        return ''.join(lines)
    
    def copy_style_files(self, output_folder: str) -> List[str]:
        """
        Copy all .sty files from the current directory to the output folder.
        
        Args:
            output_folder: Destination directory for style files
            
        Returns:
            List of copied style file names
            
        Raises:
            Exception: If file copying fails
        """
        copied_files = []
        current_dir = Path.cwd()
        output_path = Path(output_folder)
        
        try:
            # Find all .sty files in current directory
            sty_files = list(current_dir.glob("*.sty"))
            
            for sty_file in sty_files:
                dest_file = output_path / sty_file.name
                shutil.copy2(sty_file, dest_file)
                copied_files.append(sty_file.name)
                
        except (IOError, OSError) as error:
            raise Exception(f"Error copying style files: {error}")
            
        return copied_files


class TMAGeneratorGUI:
    """
    Main GUI application for TMA LaTeX Generator.
    
    Provides user interface for configuring TMA structure and generating
    LaTeX files. Includes tooltips, help system, and persistent settings.
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the main GUI application.
        
        Args:
            root: Main tkinter window
        """
        self.root = root
        self.config = ConfigManager.load_config()
        self.question_widgets: List[Dict[str, Union[ttk.Frame, tk.StringVar]]] = []
        
        self._setup_main_window()
        self._create_widgets()
    
    def _setup_main_window(self) -> None:
        """Configure main application window."""
        self.root.title("TMA LaTeX Generator")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _create_widgets(self) -> None:
        """Create and layout all GUI widgets."""
        # Main container frame
        main_frame = ttk.Frame(self.root, padding=MAIN_FRAME_PADDING)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Application title
        row = self._create_title_section(main_frame, row)
        
        # Basic settings section
        row = self._create_basic_settings_section(main_frame, row)
        
        # Question structure section
        row = self._create_question_structure_section(main_frame, row)
        
        # Action buttons section
        row = self._create_action_buttons_section(main_frame, row)
        
        # Output display section
        self._create_output_section(main_frame, row)
    
    def _create_title_section(self, parent: ttk.Frame, row: int) -> int:
        """
        Create application title section.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        title_label = ttk.Label(
            parent,
            text="TMA LaTeX Generator",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 10))
        row += 1
        
        # Separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(
            row=row, column=0, columnspan=3,
            sticky=(tk.W, tk.E), pady=(0, SEPARATOR_PADY)
        )
        row += 1
        
        return row
    
    def _create_basic_settings_section(self, parent: ttk.Frame, row: int) -> int:
        """
        Create basic settings input fields.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        # Setting field definitions with labels, config keys, widths and tooltips
        settings_fields = [
            ("Course Code:", "course", 15, "Your module code (e.g., MATH101, PHYS201, CHEM301)"),
            ("TMA Reference:", "tma_ref", 10, "TMA assignment number (e.g., 01, 02, 03, 04)"),
            ("Cut-off Date:", "cod", 15, "Assignment submission deadline (e.g., '21 January 2026', 'TBD')"),
            ("Your Name:", "name", 30, "Your full name as registered with your institution"),
            ("Student PIN:", "pin", 15, "Your student identification number (e.g., S1234567)"),
            ("LaTeX Style:", "style", 10, "LaTeX style file to use (usually 'tma' for academic assignments)"),
        ]
        
        # Create standard input fields
        for label_text, config_key, width, tooltip_text in settings_fields:
            row = self._create_labeled_entry(
                parent, row, label_text, config_key, width, tooltip_text
            )
        
        # Special handling for output directory (has browse button)
        row = self._create_output_directory_field(parent, row)
        
        # Base filename field
        row = self._create_labeled_entry(
            parent, row, "Base Filename:", "basename", 15,
            "Name for main LaTeX file (usually 'TMA'). Creates TMA.tex as main file."
        )
        
        return row
    
    def _create_labeled_entry(
        self,
        parent: ttk.Frame,
        row: int,
        label_text: str,
        config_key: str,
        width: int,
        tooltip_text: str
    ) -> int:
        """
        Create a labeled entry field with tooltip.
        
        Args:
            parent: Parent frame
            row: Current grid row
            label_text: Text for field label
            config_key: Configuration key for this field
            width: Entry widget width
            tooltip_text: Tooltip text to display
            
        Returns:
            Next available row number
        """
        # Create label
        ttk.Label(parent, text=label_text).grid(
            row=row, column=0, sticky=tk.W, pady=ENTRY_PADY
        )
        
        # Create entry field
        var = tk.StringVar(value=self.config[config_key])
        entry = ttk.Entry(parent, textvariable=var, width=width)
        entry.grid(
            row=row, column=1, sticky=tk.W,
            pady=ENTRY_PADY, padx=(5, 0)
        )
        
        # Store reference to variable
        setattr(self, f"{config_key}_var", var)
        
        # Add tooltip
        ToolTip(entry, tooltip_text)
        
        return row + 1
    
    def _create_output_directory_field(self, parent: ttk.Frame, row: int) -> int:
        """
        Create output directory field with browse button.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        # Label
        ttk.Label(parent, text="Output Directory:").grid(
            row=row, column=0, sticky=tk.W, pady=ENTRY_PADY
        )
        
        # Entry field
        self.output_var = tk.StringVar(value=self.config["output"])
        output_entry = ttk.Entry(parent, textvariable=self.output_var, width=30)
        output_entry.grid(
            row=row, column=1, sticky=(tk.W, tk.E),
            pady=ENTRY_PADY, padx=(5, 0)
        )
        ToolTip(output_entry, "Directory where LaTeX files will be created. Use Browse button or type path directly.")
        
        # Browse button
        browse_button = ttk.Button(parent, text="Browse", command=self._browse_output)
        browse_button.grid(row=row, column=2, pady=ENTRY_PADY, padx=(5, 0))
        ToolTip(browse_button, "Click to select output directory")
        
        return row + 1
    
    def _create_question_structure_section(self, parent: ttk.Frame, row: int) -> int:
        """
        Create question structure configuration section.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        # Section separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(
            row=row, column=0, columnspan=3,
            sticky=(tk.W, tk.E), pady=SEPARATOR_PADY
        )
        row += 1
        
        # Section title
        structure_label = ttk.Label(
            parent,
            text="Question Structure (Manual Input)",
            font=("Arial", 12, "bold")
        )
        structure_label.grid(row=row, column=0, columnspan=3, pady=(0, 5))
        row += 1
        
        # Control buttons
        row = self._create_structure_control_buttons(parent, row)
        
        # Scrollable area for question inputs
        row = self._create_scrollable_question_area(parent, row)
        
        return row
    
    def _create_structure_control_buttons(self, parent: ttk.Frame, row: int) -> int:
        """
        Create control buttons for question structure.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=3, pady=5)
        
        # Button definitions: (text, command, tooltip)
        buttons = [
            ("Clear All", self._clear_structure, "Remove all questions from the structure (cannot be undone!)"),
            ("Add Question", self._add_question, "Add a new question to the structure"),
            ("Help", self._show_help, "Show comprehensive help with examples and instructions"),
        ]
        
        for text, command, tooltip in buttons:
            button = ttk.Button(control_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=BUTTON_PADX)
            ToolTip(button, tooltip)
        
        return row + 1
    
    def _create_scrollable_question_area(self, parent: ttk.Frame, row: int) -> int:
        """
        Create scrollable area for question configuration widgets.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        # Canvas for scrolling
        self.structure_canvas = tk.Canvas(parent, height=200)
        self.structure_scrollbar = ttk.Scrollbar(
            parent, orient="vertical",
            command=self.structure_canvas.yview
        )
        self.structure_scrollable_frame = ttk.Frame(self.structure_canvas)
        
        # Configure scrolling
        self.structure_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.structure_canvas.configure(
                scrollregion=self.structure_canvas.bbox("all")
            )
        )
        
        self.structure_canvas.create_window(
            (0, 0), window=self.structure_scrollable_frame, anchor="nw"
        )
        self.structure_canvas.configure(
            yscrollcommand=self.structure_scrollbar.set
        )
        
        # Grid layout
        self.structure_canvas.grid(
            row=row, column=0, columnspan=2,
            sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0)
        )
        self.structure_scrollbar.grid(
            row=row, column=2,
            sticky=(tk.N, tk.S), pady=(5, 0)
        )
        
        # Add initial question
        self._add_question()
        
        return row + 1
    
    def _create_action_buttons_section(self, parent: ttk.Frame, row: int) -> int:
        """
        Create main action buttons section.
        
        Args:
            parent: Parent frame
            row: Current grid row
            
        Returns:
            Next available row number
        """
        # Section separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(
            row=row, column=0, columnspan=3,
            sticky=(tk.W, tk.E), pady=SEPARATOR_PADY
        )
        row += 1
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        # Button definitions: (text, command, tooltip)
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
        """
        Create output display section.
        
        Args:
            parent: Parent frame
            row: Current grid row
        """
        # Output label
        ttk.Label(parent, text="Output:").grid(
            row=row, column=0, sticky=tk.W, pady=(10, 0)
        )
        row += 1
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            parent, width=70, height=15
        )
        self.output_text.grid(
            row=row, column=0, columnspan=3,
            sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0)
        )
    
    def _browse_output(self) -> None:
        """Open directory browser for output directory selection."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_var.set(directory)
    
    def _show_help(self) -> None:
        """Display help dialog."""
        HelpDialog(self.root)
    
    def _save_settings(self) -> None:
        """Save current settings to configuration file."""
        config = self._get_current_config()
        
        if ConfigManager.save_config(config):
            self.config = config
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
        else:
            messagebox.showerror("Error", "Could not save settings to file.")
    
    def _get_current_config(self) -> Dict[str, str]:
        """
        Get current configuration from GUI fields.
        
        Returns:
            Configuration dictionary with current values
        """
        return {
            "course": self.course_var.get(),
            "tma_ref": self.tma_ref_var.get(),
            "cod": self.cod_var.get(),
            "name": self.name_var.get(),
            "pin": self.pin_var.get(),
            "style": self.style_var.get(),
            "output": self.output_var.get(),
            "basename": self.basename_var.get()
        }
    
    def _add_question(self) -> None:
        """Add a new question input widget to the structure."""
        question_num = len(self.question_widgets) + 1
        question_frame = ttk.LabelFrame(
            self.structure_scrollable_frame,
            text=f"Question {question_num}"
        )
        question_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Details frame for question inputs
        details_frame = ttk.Frame(question_frame)
        details_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Create question input fields
        question_data = self._create_question_input_fields(
            details_frame, question_frame
        )
        question_data['frame'] = question_frame
        
        self.question_widgets.append(question_data)
        self._update_scroll_region()
    
    def _create_question_input_fields(
        self,
        parent: ttk.Frame,
        question_frame: ttk.LabelFrame
    ) -> Dict[str, Union[tk.StringVar, ttk.Button]]:
        """
        Create input fields for a single question.
        
        Args:
            parent: Parent frame for inputs
            question_frame: Frame containing the question (for removal)
            
        Returns:
            Dictionary containing references to created widgets
        """
        # Field definitions: (label, default_value, width, tooltip)
        field_defs = [
            ("Marks:", "25", 5, "Total marks for this question (e.g., 25, 30, 15)"),
            ("Parts:", "a,b,c,d", 20, "Question parts separated by commas\nExamples: 'a,b,c,d' or 'a,b' or 'a,b,c,d,e,f'"),
            ("Subparts (part:subparts):", "", 15, "Subparts for each part using format: part:sub1,sub2\nExamples:\n'a:i,ii,iii' or 'a:i,ii;c:1,2,3'\nLeave blank if no subparts"),
        ]
        
        question_data = {}
        
        for label_text, default_val, width, tooltip in field_defs:
            # Create label
            ttk.Label(parent, text=label_text).pack(side=tk.LEFT)
            
            # Create entry with variable
            var = tk.StringVar(value=default_val)
            entry = ttk.Entry(parent, textvariable=var, width=width)
            entry.pack(side=tk.LEFT, padx=(2, 10))
            ToolTip(entry, tooltip)
            
            # Store variable reference
            field_key = label_text.split(':')[0].lower().replace(' ', '_')
            if field_key == "subparts_(part":
                field_key = "subparts"
            question_data[f"{field_key}_var"] = var
        
        # Remove button
        remove_button = ttk.Button(
            parent,
            text="Remove",
            command=lambda: self._remove_question(question_frame)
        )
        remove_button.pack(side=tk.RIGHT)
        ToolTip(remove_button, "Remove this question from the structure")
        
        return question_data
    
    def _remove_question(self, question_frame: ttk.LabelFrame) -> None:
        """
        Remove a question from the structure.
        
        Args:
            question_frame: Frame to remove
        """
        # Get question number for confirmation message
        question_text = question_frame.cget('text')
        
        # Confirm removal
        if not messagebox.askyesno(
            "Remove Question",
            f"Remove {question_text}? This cannot be undone."
        ):
            return
        
        # Remove from widgets list
        self.question_widgets = [
            q for q in self.question_widgets
            if q['frame'] != question_frame
        ]
        question_frame.destroy()
        
        # Renumber remaining questions
        for i, question_data in enumerate(self.question_widgets):
            question_data['frame'].configure(text=f"Question {i + 1}")
        
        self._update_scroll_region()
    
    def _clear_structure(self) -> None:
        """Clear all questions from the structure."""
        # Confirm destructive action
        if messagebox.askyesno(
            "Clear All Questions",
            "This will remove all questions from the structure. This cannot be undone. Continue?"
        ):
            for question_data in self.question_widgets:
                question_data['frame'].destroy()
            self.question_widgets = []
            self._update_scroll_region()
    
    def _update_scroll_region(self) -> None:
        """Update scrollable canvas scroll region."""
        self.structure_canvas.update_idletasks()
        self.structure_canvas.configure(
            scrollregion=self.structure_canvas.bbox("all")
        )
    
    def _get_manual_structure(self) -> Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]:
        """
        Extract question structure from GUI inputs.
        
        Returns:
            Dictionary containing complete question structure
        """
        structure = {}
        
        for i, question_data in enumerate(self.question_widgets):
            q_id = f"Q{i + 1}"
            
            # Get marks (with validation)
            try:
                marks = int(question_data['marks_var'].get() or 25)
            except ValueError:
                marks = 25  # Default fallback
            
            # Parse parts
            parts_text = question_data['parts_var'].get().strip()
            parts = [p.strip() for p in parts_text.split(',') if p.strip()]
            
            # Parse subparts
            subparts_dict = self._parse_subparts_string(
                question_data['subparts_var'].get().strip()
            )
            
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
    
    def _parse_subparts_string(self, subparts_text: str) -> Dict[str, Dict[str, bool]]:
        """
        Parse subparts specification string.
        
        Args:
            subparts_text: String like "a:i,ii,iii;c:1,2,3"
            
        Returns:
            Dictionary mapping parts to their subparts
        """
        subparts_dict = {}
        
        if not subparts_text:
            return subparts_dict
        
        # Split by semicolon for different parts
        for part_subparts in subparts_text.split(';'):
            if ':' not in part_subparts:
                continue
                
            part, subparts_str = part_subparts.split(':', 1)
            part = part.strip()
            
            # Split subparts by comma
            subparts = [s.strip() for s in subparts_str.split(',') if s.strip()]
            subparts_dict[part] = {s: True for s in subparts}
        
        return subparts_dict
    
    def _validate_question_structure(self) -> Optional[str]:
        """
        Validate the question structure for common errors.
        
        Returns:
            Error message if validation fails, None if validation passes
        """
        total_marks = 0
        
        for i, question_data in enumerate(self.question_widgets):
            question_num = i + 1
            
            # Get and validate marks
            marks_text = question_data['marks_var'].get().strip()
            try:
                marks = int(marks_text) if marks_text else 25
                if marks <= 0:
                    return f"Question {question_num}: Marks must be a positive number (got '{marks_text}')."
                total_marks += marks
            except ValueError:
                return f"Question {question_num}: Marks must be a valid number (got '{marks_text}')."
            
            # Get parts list
            parts_text = question_data['parts_var'].get().strip()
            parts = [p.strip().lower() for p in parts_text.split(',') if p.strip()]
            
            if not parts:
                return f"Question {question_num}: No parts specified. Please add at least one part (e.g., 'a,b,c,d')."
            
            # Check for duplicate parts
            if len(parts) != len(set(parts)):
                duplicates = [p for p in set(parts) if parts.count(p) > 1]
                return f"Question {question_num}: Duplicate parts found: {', '.join(duplicates)}. Each part should be unique."
            
            # Get subparts string
            subparts_text = question_data['subparts_var'].get().strip()
            if not subparts_text:
                continue  # No subparts to validate
            
            # Parse and validate subparts
            subparts_dict = self._parse_subparts_string(subparts_text)
            
            # Check if all referenced parts in subparts actually exist
            for subpart_part in subparts_dict.keys():
                subpart_part_lower = subpart_part.strip().lower()
                if subpart_part_lower not in parts:
                    available_parts = ', '.join(parts)
                    return (f"Question {question_num}: Subpart references part '{subpart_part}' which doesn't exist.\n"
                           f"Available parts: {available_parts}\n"
                           f"Check your subparts format: 'part:sub1,sub2;part2:sub1,sub2'")
            
            # Check for empty subparts
            for part, subpart_dict in subparts_dict.items():
                if not subpart_dict:
                    return f"Question {question_num}: Part '{part}' has no subparts specified. Either remove '{part}:' or add subparts like '{part}:' or add subparts like '{part}:i,ii,iii'."
        
        # Validate total marks
        if total_marks != 100:
            return self._handle_marks_total_mismatch(total_marks)
        
        return None  # No validation errors
    
    def _handle_marks_total_mismatch(self, total_marks: int) -> Optional[str]:
        """
        Handle case where total marks don't add up to 100.
        
        Args:
            total_marks: The actual total of all question marks
            
        Returns:
            Error message if user chooses to fix, None if user chooses to continue
        """
        num_questions = len(self.question_widgets)
        
        if total_marks < 100:
            message = (f"Total marks: {total_marks} (should be 100)\n\n"
                      f"You currently have {num_questions} question(s).\n"
                      f"The marks are {100 - total_marks} short of 100.\n\n"
                      f"Possible issues:\n"
                      f"• Too few questions - consider adding more questions\n"
                      f"• Question marks are too low - consider increasing marks per question\n\n"
                      f"Do you want to continue generating files anyway?")
        else:  # total_marks > 100
            message = (f"Total marks: {total_marks} (should be 100)\n\n"
                      f"You currently have {num_questions} question(s).\n"
                      f"The marks are {total_marks - 100} over 100.\n\n"
                      f"Possible issues:\n"
                      f"• Too many questions - consider removing some questions\n"
                      f"• Question marks are too high - consider reducing marks per question\n\n"
                      f"Do you want to continue generating files anyway?")
        
        # Ask user if they want to continue despite the mismatch
        continue_anyway = messagebox.askyesno(
            "Marks Total Warning",
            message,
            icon='warning'
        )
        
        if continue_anyway:
            return None  # User chose to continue, no error
        else:
            return f"File generation cancelled. Please adjust your questions so the total marks equal 100 (currently: {total_marks})."
    
    def _generate_files(self) -> None:
        """Generate LaTeX files based on current configuration."""
        # Clear output display
        self.output_text.delete(1.0, tk.END)
        
        # Validate input
        if not self.question_widgets:
            messagebox.showerror("Error", "Please add at least one question.")
            return
        
        try:
            # Get configuration and structure
            config = self._get_current_config()
            
            # Validate structure before generation
            validation_error = self._validate_question_structure()
            if validation_error:
                messagebox.showerror("Validation Error", validation_error)
                return
            
            structure = self._get_manual_structure()
            
            # Generate files
            success, message = self._generate_tma_files(config, structure)
            
            if success:
                # Save successful configuration
                self.config = config
                ConfigManager.save_config(self.config)
                messagebox.showinfo("Success", "TMA files generated successfully!")
            else:
                messagebox.showerror("Error", message)
                
        except Exception as error:
            error_msg = f"Unexpected error: {str(error)}"
            self.output_text.insert(tk.END, f"{error_msg}\n")
            messagebox.showerror("Error", error_msg)
    
    def _generate_tma_files(
        self,
        config: Dict[str, str],
        structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]
    ) -> Tuple[bool, str]:
        """
        Generate TMA LaTeX files from structure.
        
        Args:
            config: Configuration dictionary
            structure: Question structure dictionary
            
        Returns:
            Tuple of (success_flag, message)
        """
        try:
            generator = LaTeXFileGenerator(config)
            
            self.output_text.insert(tk.END, "Using manual question structure...\n")
            self.output_text.see(tk.END)
            self.output_text.update()
            
            # Display structure summary
            self._display_structure_summary(structure)
            
            # Prepare generation data
            parts_list, subparts_dict = self._prepare_generation_data(structure)
            
            # Create output directory
            actual_folder = generator.create_directory(config["output"])
            self.output_text.insert(tk.END, f"Created directory: {actual_folder}\n")
            self.output_text.see(tk.END)
            self.output_text.update()
            
            # Generate main LaTeX file
            generator.create_main_tex_file(
                actual_folder,
                config["basename"],
                len(structure)
            )
            
            # Generate question files
            for i, question_parts in enumerate(parts_list):
                generator.create_question_files(
                    actual_folder,
                    config["basename"],
                    str(i + 1),
                    question_parts
                )
            
            # Generate subpart files if needed
            if subparts_dict:
                generator.create_subparts(
                    actual_folder,
                    config["basename"],
                    subparts_dict
                )
            
            # Copy style files to output directory
            copied_styles = generator.copy_style_files(actual_folder)
            if copied_styles:
                self.output_text.insert(tk.END, f"Copied style files: {', '.join(copied_styles)}\n")
                self.output_text.see(tk.END)
                self.output_text.update()
            
            # Generate suggested Overleaf project name
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
    
    def _display_structure_summary(
        self,
        structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]
    ) -> None:
        """
        Display question structure summary in output.
        
        Args:
            structure: Question structure dictionary
        """
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
    
    def _prepare_generation_data(
        self,
        structure: Dict[str, Dict[str, Union[int, Dict[str, Dict[str, bool]]]]]
    ) -> Tuple[List[Tuple[str, ...]], Dict[str, int]]:
        """
        Prepare data structures for LaTeX file generation.
        
        Args:
            structure: Question structure dictionary
            
        Returns:
            Tuple of (parts_list, subparts_dict)
        """
        parts_list = []
        subparts_dict = {}
        
        for q_id in sorted(structure.keys(), key=lambda x: int(x[1:])):
            q_data = structure[q_id]
            question_parts = tuple(sorted(q_data.get('parts', {}).keys()))
            parts_list.append(question_parts)
            
            # Process subparts
            for part_id, part_data in q_data.get('parts', {}).items():
                subparts = list(part_data.get('subparts', {}).keys())
                if subparts:
                    subparts_dict[f"{QUESTION_PREFIX}{q_id[1:]}{part_id}"] = len(subparts)
        
        return parts_list, subparts_dict
    
    def _generate_overleaf_project_name(self, config: Dict[str, str]) -> str:
        """
        Generate a suggested Overleaf project name based on course details.
        
        Args:
            config: Configuration dictionary with course details
            
        Returns:
            Suggested project name string
        """
        course = config.get('course', 'COURSE').upper()
        tma_ref = config.get('tma_ref', '01').zfill(2)  # Ensure 2 digits
        cod = config.get('cod', '').strip()
        
        # Extract year from cut-off date if possible
        year_suffix = ""
        if cod:
            # Try to extract year from various date formats
            import re
            year_match = re.search(r'\b(20\d{2})\b', cod)
            if year_match:
                year_suffix = f" ({year_match.group(1)})"
        
        # Generate clean, professional project name
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