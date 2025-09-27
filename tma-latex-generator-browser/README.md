# TMA LaTeX Generator - Browser Edition

> **🎓 Professional LaTeX file structure generator for academic TMA assignments - Zero installation required!**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Try_Now!-brightgreen?style=for-the-badge)](https://gwb2025.github.io/tma-latex-generator-browser/)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Deployed-blue?style=for-the-badge&logo=github)](https://gwb2025.github.io/tma-latex-generator-browser/)
[![Overleaf Ready](https://img.shields.io/badge/Overleaf-Ready-orange?style=for-the-badge&logo=overleaf)](https://www.overleaf.com/)

[![Browser Compatible](https://img.shields.io/badge/Browser-Compatible-brightgreen?logo=googlechrome)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)
[![No Installation](https://img.shields.io/badge/Installation-None_Required-blue?logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow?logo=mit)](LICENSE)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)](script.js)
[![HTML5](https://img.shields.io/badge/HTML5-Modern-E34F26?logo=html5&logoColor=white)](index.html)
[![CSS3](https://img.shields.io/badge/CSS3-Responsive-1572B6?logo=css3&logoColor=white)](styles.css)

## 🚀 **Try It Now - No Installation Required!**

**👉 [Launch TMA Generator](https://gwb2025.github.io/tma-latex-generator-browser/) 👈**

*Works instantly in any modern browser - Chrome, Firefox, Safari, Edge*

---

## 📖 **What is This?**

The **TMA LaTeX Generator - Browser Edition** is a powerful web application that creates professional LaTeX document structures for academic **Tutor-Marked Assignments (TMAs)**. Originally designed for Open University students, it's perfect for any academic institution requiring structured LaTeX submissions.

### 🎯 **The Problem It Solves**
Creating properly structured LaTeX documents with multiple questions, parts, and subparts is time-consuming and error-prone. This tool generates the entire file structure automatically, letting you focus on writing content rather than wrestling with LaTeX formatting.

### ✨ **The Solution**
- **Configure once** - Set up your course details and question structure
- **Generate instantly** - Download a complete ZIP file with all LaTeX files
- **Upload to Overleaf** - Professional formatting and compilation ready
- **Start writing** - Focus on your answers, not file management

---

## 🌟 **Why Choose the Browser Edition?**

### ✅ **Zero Installation**
- No Python, LaTeX, or dependencies required
- Works on any device with a modern browser
- Perfect for Chromebooks, tablets, and shared computers

### ✅ **Enhanced User Experience**
- **Real-time validation** with helpful error messages
- **Auto-save functionality** - never lose your progress
- **Professional tooltips** on every field
- **Keyboard shortcuts** for power users
- **Responsive design** - works on any screen size

### ✅ **Professional Results**
- **Identical output** to the original desktop version
- **Academic-grade LaTeX** with professional styling
- **Overleaf-optimized** file structure
- **Complete style files** included (tma.sty, tma-extras.sty)

### ✅ **Privacy-First**
- **100% client-side** - no data sent to servers
- **Local storage only** - your data stays in your browser
- **No tracking** or analytics
- **Open source** - completely transparent

---

## 🎬 **Quick Start Demo**

### 1. **🌐 Open the App**
**[Click here to launch](https://gwb2025.github.io/tma-latex-generator-browser/)** or visit:
```
https://gwb2025.github.io/tma-latex-generator-browser/
```

### 2. **📝 Configure Your TMA**
Fill in your course details:
- **Course Code**: e.g., `MATH101`, `PHYS201`
- **TMA Reference**: e.g., `04`
- **Your Name**: Your full registered name
- **Cut-off Date**: e.g., `21 January 2026`

### 3. **❓ Add Questions**
For each question, specify:
- **Marks**: Total marks (e.g., `25`)
- **Parts**: Comma-separated (e.g., `a,b,c,d`)
- **Subparts**: Optional format `part:subs` (e.g., `a:i,ii,iii`)

### 4. **🚀 Generate & Download**
Click "Generate TMA Files" to download a ZIP containing all LaTeX files.

### 5. **📤 Upload to Overleaf**
- Create new blank project in Overleaf
- Delete default main.tex
- Upload all files from the ZIP
- Compile and start writing!

---

## 📚 **Example TMA Structure**

```yaml
Question 1: 
  Marks: 30
  Parts: a,b,c  
  Subparts: a:i,ii,iii;c:i,ii

Question 2:
  Marks: 25  
  Parts: a,b,c,d
  Subparts: b:1,2,3

Question 3:
  Marks: 25
  Parts: a,b,c,d  
  Subparts: (none)

Question 4:
  Marks: 20
  Parts: a,b
  Subparts: a:i,ii;b:i,ii,iii
```

**Result**: Professional LaTeX structure with 15+ files ready for Overleaf!

---

## 📁 **Generated File Structure**

```
📦 MATH101-TMA04-LaTeX-Files.zip
├── 📄 TMA.tex              # Main document (compile this)
├── 📄 q1.tex               # Question 1 structure  
├── ✏️ q1a.tex              # Q1 part (a) - EDIT THIS
├── ✏️ q1b.tex              # Q1 part (b) - EDIT THIS  
├── ✏️ q1c.tex              # Q1 part (c) - EDIT THIS
├── ✏️ q1a_0.tex            # Q1(a) subpart (i) - EDIT THIS
├── ✏️ q1a_1.tex            # Q1(a) subpart (ii) - EDIT THIS
├── ✏️ q1a_2.tex            # Q1(a) subpart (iii) - EDIT THIS
├── 📄 q2.tex               # Question 2 structure
├── ✏️ q2a.tex              # Q2 part (a) - EDIT THIS
├── 🎨 tma.sty              # Main LaTeX style file
└── 🎨 tma-extras.sty       # Extended LaTeX commands
```

✏️ = **Edit these files** for your answers  
📄 = Structure files (don't edit)  
🎨 = Style files (don't edit)

---

## 🛠️ **Features & Capabilities**

### 📋 **Smart Form Management**
- **Auto-save** - Settings saved as you type
- **Validation** - Real-time error checking  
- **Import/Export** - Save and restore configurations
- **Professional tooltips** - Help on every field

### 🎯 **Intelligent Generation**
- **Complete LaTeX structure** matching academic standards
- **Automatic file naming** following conventions
- **Professional style files** with 200+ mathematical commands
- **Overleaf project names** generated automatically

### ⌨️ **Power User Features**
- **Keyboard shortcuts**: Ctrl+G (generate), Ctrl+S (save), Ctrl+H (help)
- **Batch operations** - Add/remove multiple questions quickly
- **Live preview** - See marks totals update in real-time
- **Error prevention** - Validation before generation

### 📱 **Universal Compatibility**
- **Responsive design** - Works on desktop, tablet, mobile
- **Cross-browser** - Chrome, Firefox, Safari, Edge
- **Offline-capable** - Works without internet after first load
- **Accessibility** - Screen reader friendly, keyboard navigation

---

## 🌐 **Overleaf Integration**

### **Why Overleaf?**
- ✅ **No LaTeX installation** required
- ✅ **Real-time collaboration** with supervisors
- ✅ **Professional PDF output** 
- ✅ **Version history** and backup
- ✅ **Cross-device synchronization**
- ✅ **Rich editor** with error highlighting

### **Perfect Workflow**
1. **Generate** structure with this browser app
2. **Upload** to Overleaf for editing and compilation  
3. **Collaborate** with supervisors in real-time
4. **Submit** professional PDF directly from Overleaf

---

## 🔧 **Technical Specifications**

### **Browser Requirements**
- **Modern browsers**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **JavaScript**: ES6+ features required
- **Storage**: LocalStorage for settings persistence
- **Downloads**: File download capability required

### **Core Technologies**
- **Pure JavaScript** - No frameworks, maximum compatibility
- **Modern CSS** - CSS Grid, Flexbox, CSS Variables
- **HTML5** - Semantic markup and modern APIs
- **JSZip** - Client-side ZIP file generation

### **Architecture Highlights**
- **Modular design** - Clean separation of concerns
- **Memory efficient** - Debounced operations, optimized DOM
- **Error resilient** - Comprehensive error handling
- **Performance optimized** - Fast loading, responsive UI

---

## 📖 **Documentation**

### **Usage Examples**

**Simple Question**:
```
Marks: 25
Parts: a,b,c,d  
Subparts: (blank)
```
Creates Q1 with 4 parts, no subparts.

**Complex Question**:
```  
Marks: 30
Parts: a,b,c
Subparts: a:i,ii,iii;c:1,2
```
Creates Q1(a) with 3 subparts, Q1(b) simple, Q1(c) with 2 subparts.

### **Field Reference**

| Field | Format | Example |
|-------|--------|---------|
| **Course Code** | UPPERCASE | `MATH101`, `PHYS201` |
| **TMA Reference** | 2-digit number | `01`, `04` |
| **Parts** | Comma-separated | `a,b,c,d` |
| **Subparts** | `part:sub1,sub2;part2:sub1` | `a:i,ii,iii;c:1,2` |

### **Keyboard Shortcuts**

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` | Generate TMA Files |
| `Ctrl+S` | Save Settings |
| `Ctrl+H` | Show Help |
| `Esc` | Close Help Dialog |

---

## 🚀 **Getting Started for Developers**

### **Local Development**

```bash
# Clone the repository
git clone https://github.com/GWB2025/tma-latex-generator-browser.git
cd tma-latex-generator-browser

# Serve locally (choose one method)
python -m http.server 8080    # Python
npx serve .                   # Node.js  
php -S localhost:8080         # PHP

# Open in browser
open http://localhost:8080
```

### **File Structure**
```
📂 tma-latex-generator-browser/
├── 📄 index.html           # Main application (178 lines)
├── 🎨 styles.css           # Complete styling (764 lines)
├── ⚙️ script.js            # Application logic (1,413 lines)
├── 📄 tma.sty              # LaTeX main style file
├── 📄 tma-extras.sty       # Extended LaTeX commands
├── 📄 README.md            # This documentation
├── 📄 LICENSE              # MIT License
└── 📄 .gitignore           # Git ignore patterns
```

### **Key JavaScript Modules**
- **CONFIG** - Application configuration constants
- **State** - Global application state management  
- **Utils** - Utility functions and helpers
- **Storage** - LocalStorage and settings persistence
- **Tooltip** - Interactive help system
- **Validation** - Input validation and error handling
- **LaTeXGenerator** - Core file generation engine
- **UI** - User interface management and events

---

## 🤝 **Contributing**

We welcome contributions! This project maintains high standards:

### **Development Guidelines**
- **Code Quality**: Professional JavaScript with JSDoc documentation
- **User Experience**: Intuitive interface with comprehensive help
- **Compatibility**: Cross-browser support for modern browsers  
- **Performance**: Memory-efficient, optimized operations

### **How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Areas for Contribution**
- 🌐 **Internationalization** - Multi-language support
- 🎨 **Themes** - Dark mode, accessibility themes
- 📱 **Mobile UX** - Enhanced mobile experience
- 🔧 **LaTeX Features** - Additional LaTeX templates
- 📊 **Analytics** - Usage insights (privacy-preserving)

---

## 🎓 **Educational Impact**

### **Perfect For**
- **🎓 Students** - No technical setup required
- **🏫 Institutions** - Zero-install solution for labs
- **💻 Chromebook users** - Full functionality in browser
- **📱 Mobile learners** - Works on tablets and phones
- **🌍 Remote education** - Accessible anywhere with internet

### **Academic Benefits**
- **⚡ Quick setup** - Start writing immediately
- **📐 Professional formatting** - Academic-grade LaTeX output
- **🤝 Collaboration-ready** - Overleaf integration
- **📚 Reusable** - Save configurations for future TMAs
- **🔄 Version control** - Git-friendly LaTeX source files

---

## 📊 **Comparison: Desktop vs Browser**

| Feature | Desktop Version | Browser Version |
|---------|-----------------|-----------------|
| **Installation** | Python Required | ✅ None Required |
| **Accessibility** | Platform Limited | ✅ Universal |
| **Updates** | Manual Download | ✅ Always Latest |
| **Mobile Support** | ❌ No | ✅ Responsive Design |
| **Sharing** | File Transfer | ✅ URL Sharing |
| **Collaboration** | Limited | ✅ Overleaf Integration |
| **Storage** | File System | Browser LocalStorage |
| **Privacy** | ✅ Complete | ✅ Client-side Only |

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### **What This Means**
- ✅ **Free to use** for personal and commercial purposes
- ✅ **Modify and distribute** freely
- ✅ **No warranty** - use at your own risk
- ✅ **Attribution appreciated** but not required

---

## 🙏 **Acknowledgments**

- **Academic Community** - For LaTeX standards and style requirements
- **Open University** - Inspiration for TMA structure and workflow
- **Overleaf Team** - For making LaTeX accessible to everyone
- **JavaScript Community** - For excellent tools and libraries
- **Contributors** - Everyone who helps improve this tool

---

## 📞 **Support & Contact**

### **Getting Help**
- 📚 **Documentation**: This README and in-app help system
- 💬 **Issues**: [GitHub Issues](https://github.com/GWB2025/tma-latex-generator-browser/issues)
- 🤝 **Discussions**: [GitHub Discussions](https://github.com/GWB2025/tma-latex-generator-browser/discussions)

### **Quick Links**
- 🌐 **Live Demo**: https://gwb2025.github.io/tma-latex-generator-browser/
- 📦 **Repository**: https://github.com/GWB2025/tma-latex-generator-browser
- 🖥️ **Desktop Version**: https://github.com/GWB2025/tma-latex-generator
- 🍃 **Overleaf**: https://www.overleaf.com/

---

## 🌟 **Star This Repository**

If this tool helps you create better academic documents, please **⭐ star this repository** to help others discover it!

**[⭐ Star on GitHub](https://github.com/GWB2025/tma-latex-generator-browser)** | **[🌐 Try Live Demo](https://gwb2025.github.io/tma-latex-generator-browser/)** | **[📖 View Documentation](README.md)**

---

<div align="center">

**Made with ❤️ for students worldwide**

*Empowering academic excellence through technology*

**[🚀 Launch TMA Generator Now](https://gwb2025.github.io/tma-latex-generator-browser/)**

</div>