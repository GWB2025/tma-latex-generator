# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python utility for generating LaTeX files for academic Tutor-Marked Assignments (TMAs), specifically designed for Overleaf workflow. The tool provides manual input methods for creating structured TeX files with proper organisation and templating, ready for upload to Overleaf.

### Key Features
- **Manual Question Structure Input**: Robust GUI interface for manually specifying question structure
- **Auto-Detection from PDF**: Optional PDF parsing to pre-populate question structure  
- **Flexible Structure Support**: Handles questions with multiple parts and subparts
- **LaTeX Generation**: Creates complete directory structure with proper TeX files for Overleaf

## Architecture

### Core Components

- **tma_generator_gui.py**: Main GUI application with manual input interface
- **Configuration Management**: JSON-based config storage for user preferences
- **LaTeX Generation Engine**: Creates structured TeX files with proper includes and formatting

### Key Functions

1. **Manual Input Interface**:
   - Dynamic question widgets with add/remove functionality
   - Support for specifying parts (a,b,c,d) and subparts (i,ii,iii or 1,2,3)
   - Marks allocation per question
   - Scrollable interface for multiple questions

2. **PDF Auto-Detection** (optional):
   - Extracts text from PDF using PyPDF2
   - Attempts to identify question structure automatically
   - Pre-populates manual input fields
   - Falls back gracefully if extraction fails

3. **LaTeX Generation**:
   - Creates main document with student info
   - Generates individual question files
   - Creates part and subpart files as needed
   - Handles proper TeX root directives
   - Automatically copies .sty files for Overleaf compatibility

## Common Commands

### Running the Application

```powershell
# Run the GUI application
python tma_generator_gui.py

# The application will start with a manual input interface
```

### Using the Manual Input Interface

1. **Basic Setup**: Fill in student details, course info, and output directory
2. **Question Structure**: 
   - Use "Add Question" to add more questions
   - Enter parts as comma-separated: `a,b,c,d`
   - Enter subparts as `part:subparts` format: `a:i,ii,iii`
   - Set marks for each question
3. **Generate Files**: Click "Generate TMA Files"

### Using Auto-Detection (Optional)

1. **Select PDF**: Choose your TMA PDF file
2. **Auto-Detect**: Click "Auto-Detect from PDF" button
3. **Review/Edit**: Check the populated structure and modify as needed
4. **Generate**: Click "Generate TMA Files"

### Manual Input Format Examples

- **Parts**: `a,b,c,d` or `a,b,c,d,e`
- **Subparts**: `a:i,ii;b:1,2,3` (part a has subparts i,ii; part b has subparts 1,2,3)
- **Marks**: Any integer (default: 25)

## File Structure Generated (Overleaf-Ready)

```
output_directory/
├── TMA.tex                 # Main document (Overleaf main file)
├── q1.tex                  # Question 1 structure
├── q1a.tex                 # Question 1, part (a)
├── q1b.tex                 # Question 1, part (b)
├── q1a_0.tex              # Question 1a, subpart 0 (if subparts exist)
├── q1a_1.tex              # Question 1a, subpart 1
├── tma.sty                 # LaTeX style file (automatically copied)
├── tma-extras.sty          # Extended LaTeX styles (automatically copied)
└── ...                     # Additional questions and parts
```

## Overleaf Workflow

1. **Generate files** using this tool
2. **Create blank Overleaf project**
3. **Delete default main.tex** in Overleaf
4. **Upload entire output directory** contents to Overleaf
5. **Compile and edit** your TMA directly in Overleaf

## Configuration

The application uses `tma_generator_config.json` for persistent settings:
- Student information (name, PIN)
- Course details
- File paths and preferences
- Last used settings

## Dependencies

- Python 3.x with tkinter (GUI)
- PyPDF2 (for optional PDF extraction)
- pathlib, re, json (standard library)

## Development Notes

- **Robustness**: Manual input ensures 100% accuracy vs unreliable PDF parsing
- **Flexibility**: Supports any question structure the user specifies
- **User Experience**: GUI provides immediate visual feedback
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Extensibility**: Easy to add new input formats or LaTeX templates

## Troubleshooting

- **PDF Auto-Detection Issues**: Use manual input instead - it's more reliable
- **LaTeX Compilation**: Ensure you have the `tma.sty` package available
- **File Generation Errors**: Check output directory permissions
- **GUI Display Issues**: Increase window size if elements are cramped