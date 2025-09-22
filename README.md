# TMA LaTeX Generator

> **Professional LaTeX file structure generator for Open University TMA (Tutor-Marked Assignment) submissions**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue)](https://peps.python.org/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

The TMA LaTeX Generator is a professional GUI application that creates structured LaTeX file hierarchies for Open University assignments. Instead of manually creating multiple interconnected LaTeX files, this tool generates the complete structure based on your question configuration.

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
- Open University LaTeX style files (`tma.sty`)

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

## 📖 Usage

### Basic Configuration

1. **Course Information:**
   - **Course Code**: Your OU module (e.g., M840-AAT, M336)
   - **TMA Reference**: Assignment number (01, 02, 03, 04)
   - **Cut-off Date**: Submission deadline
   - **Your Name**: Full name as registered with OU
   - **Student PIN**: Your OU identification number

2. **Question Structure:**
   - **Marks**: Total marks per question (e.g., 25, 30)
   - **Parts**: Question parts separated by commas (e.g., "a,b,c,d")
   - **Subparts**: Format: `part:subparts` (e.g., "a:i,ii,iii;c:1,2,3")

### Example Structure

For a typical OU TMA with complex subparts:

```
Question 1: Marks=30, Parts=a,b,c, Subparts=a:i,ii,iii;c:i,ii
Question 2: Marks=25, Parts=a,b,c,d, Subparts=b:1,2,3
Question 3: Marks=25, Parts=a,b,c,d, Subparts=(blank)
Question 4: Marks=20, Parts=a,b, Subparts=a:i,ii;b:i,ii,iii
```

### Generated Files

The application creates:
- **TMA.tex**: Main LaTeX document
- **q1.tex, q2.tex, ...**: Individual question files
- **q1a.tex, q1b.tex, ...**: Question part files
- **q1a_0.tex, q1a_1.tex, ...**: Subpart files (when applicable)

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
- **OU Style Compatible**: Works with official OU LaTeX styles
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Open University**: For providing the educational context and LaTeX style requirements
- **Python Community**: For the excellent tkinter framework and development tools
- **Contributors**: Thanks to all who have contributed to making this tool better

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GWB2025/tma-latex-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GWB2025/tma-latex-generator/discussions)
- **Documentation**: Built-in help system (Help button in application)

## 🎓 Educational Use

This tool is specifically designed for Open University students working on Tutor-Marked Assignments (TMAs). It streamlines the LaTeX document preparation process, allowing students to focus on content rather than file structure management.

**Note**: This tool generates the LaTeX structure only. You'll need:
- A LaTeX editor (TeXstudio, TeXworks, Overleaf, etc.)
- OU LaTeX style files (`tma.sty`)
- Basic LaTeX knowledge for content creation

---

**Made with ❤️ for OU students by the community**