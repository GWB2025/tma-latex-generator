# TMA LaTeX Generator

> **Professional LaTeX file structure generator for academic TMA (Tutor-Marked Assignment) submissions**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://peps.python.org/pep-0008/)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licences/MIT)

## 🎯 Overview

The TMA LaTeX Generator is a professional GUI application that creates structured LaTeX file hierarchies for academic assignments, specifically designed for use with **Overleaf**. Instead of manually creating multiple interconnected LaTeX files, this tool generates the complete structure based on your question configuration, ready to upload to Overleaf.

### ✨ Key Features

- **📋 Intuitive GUI**: Easy-to-use interface with tooltips and comprehensive help
- **🔧 Manual Structure Configuration**: Define questions, parts, and subparts precisely
- **📁 Complete File Generation**: Creates main document and all component files
- **⚙️ Persistent Settings**: Saves your configuration for future use
- **🎨 Professional Code Quality**: PEP 8 compliant, fully documented, type-hinted

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- tkinter (usually included with Python)
- Overleaf account (free or paid)
- Academic LaTeX style files (included: `tma.sty`, `tma-extras.sty`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GWB2025/tma-latex-generator.git
   cd tma-latex-generator
   ```

2. **Run the application:**
   ```bash
   python tma_generator_gui.py
   ```

3. **Configure your TMA:**
   - Fill in course details (Course Code, TMA Reference, etc.)
   - Set up question structure (marks, parts, subparts)
   - Choose output directory
   - Click "Generate TMA Files"

4. **Upload to Overleaf:**
   - Create a new blank project in Overleaf
   - Delete the default files (main.tex, etc.)
   - Upload all files from your output directory
   - Compile and start writing!

## 📖 Usage

### Basic Configuration

1. **Course Information:**
   - **Course Code**: Your module (e.g., MATH101, PHYS201)
   - **TMA Reference**: Assignment number (01, 02, 03, 04)
   - **Cut-off Date**: Submission deadline
   - **Your Name**: Full name as registered with your institution
   - **Student PIN**: Your student identification number

2. **Question Structure:**
   - **Marks**: Total marks per question (e.g., 25, 30)
   - **Parts**: Question parts separated by commas (e.g., "a,b,c,d")
   - **Subparts**: Format: `part:subparts` (e.g., "a:i,ii,iii;c:1,2,3")

### Example Structure

For a typical academic TMA with complex subparts:

```
Question 1: Marks=30, Parts=a,b,c, Subparts=a:i,ii,iii;c:i,ii
Question 2: Marks=25, Parts=a,b,c,d, Subparts=b:1,2,3
Question 3: Marks=25, Parts=a,b,c,d, Subparts=(blank)
Question 4: Marks=20, Parts=a,b, Subparts=a:i,ii;b:i,ii,iii
```

### Generated Files

The application creates a complete file structure ready for Overleaf:
- **TMA.tex**: Main LaTeX document
- **q1.tex, q2.tex, ...**: Individual question files
- **q1a.tex, q1b.tex, ...**: Question part files
- **q1a_0.tex, q1a_1.tex, ...**: Subpart files (when applicable)
- **tma.sty, tma-extras.sty**: LaTeX style files (automatically copied)

## 🌍 Using with Overleaf

This tool is specifically designed for Overleaf workflow:

### Step 1: Generate Files
1. Run the TMA LaTeX Generator
2. Configure your assignment details
3. Set up question structure
4. Click "Generate TMA Files"
5. Note the output directory location

### Step 2: Create Overleaf Project
1. Go to [overleaf.com](https://overleaf.com) and sign in
2. Click **"New Project"** → **"Blank Project"**
3. Give your project a name (e.g., "MATH101 TMA 04")

### Step 3: Replace Default Files
1. **Delete** the default `main.tex` file in Overleaf
2. **Upload** all files from your output directory:
   - Use the upload button or drag & drop
   - Upload all `.tex` and `.sty` files together
   - Overleaf will automatically detect the file structure

### Step 4: Compile and Edit
1. **Set main document**: Ensure `TMA.tex` is set as the main document
2. **Compile**: Click the green "Recompile" button
3. **Start writing**: Edit the individual question part files (`q1a.tex`, `q1b.tex`, etc.)
4. **Preview**: View your formatted TMA in the PDF preview

### Overleaf Benefits
- ✅ **No local LaTeX installation** required
- ✅ **Automatic compilation** with error highlighting
- ✅ **Real-time preview** of your formatted document
- ✅ **Cloud storage** – never lose your work
- ✅ **Collaboration** features for group assignments
- ✅ **Version history** and backup
- ✅ **Professional formatting** with included style files

## 🛠️ Features

### User Interface
- **Comprehensive Tooltips**: Hover guidance on every field
- **Help System**: Modal dialog with examples and troubleshooting
- **Configuration Persistence**: Automatically saves and restores settings
- **Error Validation**: Input validation with helpful error messages

### Code Quality
- **PEP 8 Compliant**: Professional Python coding standards
- **Type Hints**: Complete type annotation for IDE support  
- **Comprehensive Documentation**: 100% docstring coverage
- **Modular Architecture**: Clean separation of concerns

### LaTeX Integration
- **Academic Style Compatible**: Works with standard academic LaTeX styles
- **Flexible Structure**: Supports various question/part configurations
- **Professional Output**: Generates publication-ready LaTeX structure

## 📚 Documentation

- **[UI_ENHANCEMENTS.md](UI_ENHANCEMENTS.md)**: User interface improvements and tooltip system
- **[CODE_QUALITY_IMPROVEMENTS.md](CODE_QUALITY_IMPROVEMENTS.md)**: Technical improvements and architecture
- **[CHANGES.md](CHANGES.md)**: Change history and removed features
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)**: Repository setup and deployment guide

## 🏗️ Architecture

```
tma_generator_gui.py
├── ConfigManager          # Configuration file handling
├── LaTeXFileGenerator     # LaTeX file creation logic
├── TMAGeneratorGUI        # Main application interface
├── ToolTip               # UI tooltip system
└── HelpDialog            # Comprehensive help system
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/GWB2025/tma-latex-generator.git
cd tma-latex-generator

# Install development dependencies
pip install -r requirements-dev.txt  # if created

# Run tests
python -m pytest  # if tests added

# Check code quality
python -m flake8 tma_generator_gui.py
```

## 📄 Licence

This project is licensed under the MIT Licence - see the [LICENCE](LICENCE) file for details.

## 🙏 Acknowledgments

- **Academic Community**: For providing the educational context and LaTeX style requirements
- **Python Community**: For the excellent tkinter framework and development tools
- **Contributors**: Thanks to all who have contributed to making this tool better

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GWB2025/tma-latex-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GWB2025/tma-latex-generator/discussions)
- **Documentation**: Built-in help system (Help button in application)

## 🎓 Educational Use

This tool is specifically designed for students working on Tutor-Marked Assignments (TMAs). It streamlines the LaTeX document preparation process, allowing students to focus on content rather than file structure management.

**Note**: This tool generates the LaTeX structure only. You'll need:
- A LaTeX editor (TeXstudio, TeXworks, Overleaf, etc.)
- Academic LaTeX style files (`tma.sty`)
- Basic LaTeX knowledge for content creation

---

**Made with ❤️ for students by the community**
