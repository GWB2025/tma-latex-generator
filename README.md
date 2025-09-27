# TMA LaTeX Generator

> **Professional LaTeX file structure generator for academic TMA (Tutor-Marked Assignment) submissions**
> 
> 🌐 **NEW**: Now available as a **zero-installation browser app** alongside the original desktop version!

[![Live Browser App](https://img.shields.io/badge/🌐_Browser_App-Try_Now!-brightgreen?style=for-the-badge)](https://gwb2025.github.io/tma-latex-generator/)
[![Python Desktop](https://img.shields.io/badge/🖥️_Desktop_App-Download-blue?style=for-the-badge&logo=python)](https://github.com/GWB2025/tma-latex-generator/releases)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://peps.python.org/pep-0008/)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licences/MIT)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Live-success?logo=github)](https://gwb2025.github.io/tma-latex-generator/)

## 🎯 Overview

The TMA LaTeX Generator creates structured LaTeX file hierarchies for academic assignments, specifically designed for use with **Overleaf**. Instead of manually creating multiple interconnected LaTeX files, this tool generates the complete structure based on your question configuration, ready to upload to Overleaf.

### 🚀 **Two Ways to Use This Tool**

| 🌐 **Browser Version** | 🖥️ **Desktop Version** |
|------------------------|-------------------------|
| ✅ **No installation required** | ⚙️ **Local Python application** |
| ✅ **Works on any device** | 🖥️ **Desktop GUI with tkinter** |
| ✅ **Always up-to-date** | 📁 **File system integration** |
| ✅ **Mobile-friendly** | 🔒 **Complete offline operation** |
| **[🌐 Launch Browser App](https://gwb2025.github.io/tma-latex-generator/)** | **[📥 Download Desktop App](#-desktop-version-installation)** |

### ✨ Key Features (Both Versions)

- **📋 Intuitive Interface**: Easy-to-use with tooltips and comprehensive help
- **🔧 Precise Structure Configuration**: Define questions, parts, and subparts exactly as needed
- **📁 Complete File Generation**: Creates main document and all component files
- **⚙️ Persistent Settings**: Saves your configuration for future use
- **🎨 Professional LaTeX Output**: Academic-grade formatting with comprehensive style files
- **🌍 Overleaf Integration**: Optimised workflow for cloud-based LaTeX editing
- **📱 Universal Access**: Browser version works on any device, anywhere

## 🚀 Quick Start

### 🌐 **Browser Version (Recommended for New Users)**

**No installation required! Works immediately in any modern browser.**

1. **🌐 Open the Browser App:**
   **👉 [Launch TMA Generator](https://gwb2025.github.io/tma-latex-generator/) 👈**

2. **📝 Configure your TMA:**
   - Fill in course details (Course Code, TMA Reference, Your Name, Cut-off Date)
   - Set up question structure (marks, parts, subparts)
   - Settings automatically saved in your browser

3. **🚀 Generate & Download:**
   - Click "Generate TMA Files" to download ZIP file
   - Contains all LaTeX files ready for Overleaf

4. **📤 Upload to Overleaf:**
   - Create new blank project in Overleaf
   - Upload all files from the downloaded ZIP
   - Compile and start writing!

---

### 🖥️ **Desktop Version Installation**

**For users who prefer local desktop applications:**

#### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- Overleaf account (free or paid)

#### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GWB2025/tma-latex-generator.git
   cd tma-latex-generator
   ```

2. **Run the desktop application:**
   ```bash
   python tma_generator_gui.py
   ```

3. **Configure and generate:**
   - Fill in course details and question structure
   - Choose output directory
   - Click "Generate TMA Files"
   - Upload generated files to Overleaf

---

## 🌟 **Which Version Should You Choose?**

### ✅ **Choose Browser Version If You:**
- Want **immediate access** without any setup
- Use **multiple devices** (laptop, tablet, phone)
- Work on **Chromebooks** or shared computers
- Prefer **always up-to-date** applications
- Need **mobile accessibility** for quick edits
- Want **zero maintenance** and automatic updates

### ✅ **Choose Desktop Version If You:**
- Prefer **traditional desktop applications**
- Need **complete offline operation**
- Want **deep file system integration**
- Have **specific Python workflow requirements**
- Prefer **local file management** over browser downloads

---

## 📖 Usage (Both Versions)

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
5. Note the output directory location and suggested project name

### Step 2: Create Overleaf Project
1. Go to [overleaf.com](https://overleaf.com) and sign in
2. Click **"New Project"** → **"Blank Project"**
3. Use the suggested project name from the generator output
   - Format: **"COURSE TMA XX (YEAR)"** (e.g., "MATH101 TMA 04 (2026)")
   - Automatically generated from your course details

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

## 🖥️ Using with TeX Live (Local Installation)

For users who prefer working locally with TeX Live instead of Overleaf:

### Prerequisites
- **TeX Live** installed on your system ([Download TeX Live](https://tug.org/texlive/))
- **LaTeX Editor** (TeXstudio, TeXworks, VS Code with LaTeX Workshop, etc.)
- Basic familiarity with command-line LaTeX compilation

### Step 1: Generate Files
1. Run the TMA LaTeX Generator
2. Configure your assignment details
3. Set up question structure  
4. Choose a local output directory
5. Click "Generate TMA Files"

### Step 2: Navigate to Output Directory
```bash
# Navigate to your chosen output directory
cd /path/to/your/output/directory

# Verify all files are present
ls -la
# Should show: TMA.tex, q1.tex, q2.tex, ..., tma.sty, tma-extras.sty
```

### Step 3: Compile with TeX Live

#### Option A: Using pdflatex (Recommended)
```bash
# Compile the main document
pdflatex TMA.tex

# If you have citations/references, run:
pdflatex TMA.tex
bibtex TMA        # Only if you have references
pdflatex TMA.tex
pdflatex TMA.tex
```

#### Option B: Using latexmk (Automated)
```bash
# Automated compilation with dependency handling
latexmk -pdf TMA.tex

# For continuous compilation (rebuilds on file changes)
latexmk -pdf -pvc TMA.tex
```

#### Option C: Using xelatex/lualatex
```bash
# For advanced font support or Unicode
xelatex TMA.tex
# or
lualatex TMA.tex
```

### Step 4: Edit and Work Locally

1. **Open in Your LaTeX Editor:**
   - Load `TMA.tex` as the main document
   - Edit individual files (`q1a.tex`, `q1b.tex`, etc.) for your answers
   - Use your editor's build system or compile manually

2. **File Structure Understanding:**
   ```
   output-directory/
   ├── TMA.tex           ← Main document (compile this)
   ├── q1.tex            ← Question 1 master file
   ├── q1a.tex           ← Question 1, part (a) - EDIT THIS
   ├── q1b.tex           ← Question 1, part (b) - EDIT THIS
   ├── q2.tex            ← Question 2 master file
   ├── q2a.tex           ← Question 2, part (a) - EDIT THIS
   ├── tma.sty           ← Style file (don't edit)
   └── tma-extras.sty    ← Additional styles (don't edit)
   ```

3. **Editing Workflow:**
   - **Don't edit** `TMA.tex` or `q1.tex, q2.tex` (these are structure files)
   - **Do edit** the part files: `q1a.tex`, `q1b.tex`, `q2a.tex`, etc.
   - Add your mathematical content, text, figures, etc. in the part files

### TeX Live Troubleshooting

#### Common Issues:

**Error: "File `tma.sty' not found"**
```bash
# Ensure .sty files are in the same directory as TMA.tex
# Or install them in your local texmf tree:
mkdir -p ~/texmf/tex/latex/local
cp tma.sty tma-extras.sty ~/texmf/tex/latex/local/
texhash ~/texmf
```

**Compilation Errors:**
```bash
# Check for LaTeX syntax errors in your part files
# Use your editor's syntax highlighting and error checking
# Compile with verbose output:
pdflatex -interaction=nonstopmode TMA.tex
```

**Missing Dependencies:**
```bash
# Install additional LaTeX packages if needed
# TeX Live users:
tlmgr install package-name

# Ubuntu/Debian users:
sudo apt install texlive-latex-extra texlive-math-extra

# macOS users (with MacTeX):
# Packages usually included, use TeX Live Utility if needed
```

### TeX Live vs Overleaf Comparison

| Feature | TeX Live (Local) | Overleaf (Cloud) |
|---------|-----------------|------------------|
| **Setup** | Requires installation | Browser-based |
| **Internet** | Offline capable | Requires internet |
| **Performance** | Fast local compilation | Depends on connection |
| **Storage** | Your local disk | Cloud storage |
| **Collaboration** | Manual file sharing | Built-in sharing |
| **Package Management** | Manual (tlmgr) | Automatic |
| **Backup** | Your responsibility | Automatic |
| **Privacy** | Completely local | Cloud-based |
| **Cost** | Free (after installation) | Free/Paid tiers |

**Choose TeX Live if you:**
- Prefer working offline
- Want maximum control over your LaTeX environment
- Have limited/unreliable internet
- Work with sensitive/confidential content
- Need specific LaTeX packages or configurations

**Choose Overleaf if you:**
- Want zero setup requirements
- Need collaboration features
- Prefer automatic backups
- Work on multiple devices
- Want real-time preview and error highlighting

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

### 🌐 **Browser Version Documentation**
- **📖 [Complete Browser Documentation](tma-latex-generator-browser/README.md)**
- **🌐 [Live Demo & Help](https://gwb2025.github.io/tma-latex-generator/)** - In-app help system
- **⌨️ Keyboard Shortcuts**: Ctrl+H for help, Ctrl+G to generate, Ctrl+S to save

### 🖥️ **Desktop Version Documentation**
- **📖 This README** - Complete desktop usage guide
- **🔘 Built-in Help**: Click the "Help" button in the desktop application
- **💡 Tooltips**: Hover guidance on every field

### 🤝 **Community Support**
- **🐛 [Report Issues](https://github.com/GWB2025/tma-latex-generator/issues)**
- **💬 [Discussions](https://github.com/GWB2025/tma-latex-generator/discussions)**
- **📧 Feature Requests**: Via GitHub Issues

## 🏗️ Architecture

### 🖥️ **Desktop Version (Python)**
```
tma_generator_gui.py
├── ConfigManager          # Configuration file handling
├── LaTeXFileGenerator     # LaTeX file creation logic
├── TMAGeneratorGUI        # Main application interface
├── ToolTip               # UI tooltip system
└── HelpDialog            # Comprehensive help system
```

### 🌐 **Browser Version (JavaScript)**
```
tma-latex-generator-browser/
├── index.html             # Main application interface
├── script.js              # Complete application logic (1,400+ lines)
│   ├── CONFIG            # Application constants
│   ├── State             # Global state management
│   ├── Utils             # Utility functions
│   ├── Storage           # LocalStorage persistence
│   ├── Tooltip           # Interactive help system
│   ├── Validation        # Input validation engine
│   ├── LaTeXGenerator    # File generation engine
│   └── UI                # User interface management
├── styles.css            # Complete responsive styling (750+ lines)
├── tma.sty               # LaTeX main style file
└── tma-extras.sty        # Extended LaTeX commands
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

## 📞 Support & Links

### 🌐 **Browser Version**
- **🚀 [Live Application](https://gwb2025.github.io/tma-latex-generator/)**
- **📖 [Browser Documentation](tma-latex-generator-browser/README.md)**
- **💡 In-app Help**: Press Ctrl+H or click Help button

### 🖥️ **Desktop Version**
- **📥 [Download/Clone](https://github.com/GWB2025/tma-latex-generator)**
- **💡 Built-in Help**: Help button in desktop application
- **📖 Documentation**: This README file

### 🤝 **Community**
- **🐛 [Issues](https://github.com/GWB2025/tma-latex-generator/issues)** - Bug reports & feature requests
- **💬 [Discussions](https://github.com/GWB2025/tma-latex-generator/discussions)** - Community support
- **⭐ [Star this repo](https://github.com/GWB2025/tma-latex-generator)** - If this tool helps you!

## 🎓 Educational Use

This tool is specifically designed for students working on Tutor-Marked Assignments (TMAs). It streamlines the LaTeX document preparation process, allowing students to focus on content rather than file structure management.

**Note**: This tool generates the LaTeX structure only. You'll need:

**For Overleaf users:**
- Overleaf account (free or paid)
- Web browser
- Basic LaTeX knowledge for content creation

**For TeX Live users:**
- TeX Live installation ([Download here](https://tug.org/texlive/))
- LaTeX editor (TeXstudio, TeXworks, VS Code with LaTeX Workshop, etc.)
- Academic LaTeX style files (`tma.sty`, `tma-extras.sty`) - automatically included
- Basic LaTeX knowledge for content creation

### 🌟 **Quick Links Summary**

| Resource | Browser Version | Desktop Version |
|----------|----------------|------------------|
| **🚀 Launch/Download** | **[Try Now](https://gwb2025.github.io/tma-latex-generator/)** | **[Download](https://github.com/GWB2025/tma-latex-generator)** |
| **📖 Documentation** | **[Browser README](tma-latex-generator-browser/README.md)** | **This README** |
| **💡 Help System** | In-app (Ctrl+H) | In-app (Help button) |
| **🎯 Best For** | Quick access, mobile, any device | Desktop users, offline work |

---

<div align="center">

**Made with ❤️ for students worldwide**

*Empowering academic excellence through technology*

**[🌐 Try Browser Version](https://gwb2025.github.io/tma-latex-generator/)** • **[🖥️ Use Desktop Version](#-desktop-version-installation)** • **[⭐ Star This Repo](https://github.com/GWB2025/tma-latex-generator)**

</div>
<!-- GitHub Pages configured: 2025-09-27 18:20:12 -->
