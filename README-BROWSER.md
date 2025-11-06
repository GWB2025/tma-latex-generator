# TMA LaTeX Generator - Browser Edition

> **Professional LaTeX file structure generator for academic TMA assignments - Now in your browser!**

[![Browser Compatible](https://img.shields.io/badge/browser-compatible-brightgreen)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)
[![No Installation](https://img.shields.io/badge/installation-none%20required-blue)](#)
[![Overleaf Ready](https://img.shields.io/badge/Overleaf-ready-orange)](https://www.overleaf.com/)

## 🌟 Browser Edition Features

The **Browser Edition** brings all the power of the TMA LaTeX Generator directly to your web browser with enhanced features:

### ✨ **Zero Installation Required**
- Works in any modern web browser
- No Python installation needed
- No dependencies to manage
- Instant access from any device

### 🚀 **Enhanced User Experience**
- **Real-time validation** with helpful error messages
- **Auto-save functionality** - never lose your progress
- **Keyboard shortcuts** for power users
- **Responsive design** - works on desktop, tablet, and mobile
- **Dark mode support** (respects system preference)
- **Professional notifications** system

### 💾 **Advanced Data Management**
- **Persistent storage** - settings saved automatically
- **Import/Export settings** as JSON files
- **Local storage** - all data stays in your browser
- **No server communication** - complete privacy

### 🎯 **Improved Workflow**
- **Live preview** of question structure
- **Instant feedback** on marks totals
- **Smart validation** prevents common errors
- **Professional ZIP download** with all files
- **Suggested Overleaf project names**

## 🚀 Quick Start

### 1. **Open the Application**
Simply open `index.html` in any modern web browser:

```bash
# Option 1: Double-click the file in your file explorer
# Option 2: Serve locally (recommended for development)
python -m http.server 8080  # Python 3
# Then open: http://localhost:8080

# Option 3: Use any local server
npx serve .  # Node.js
php -S localhost:8080  # PHP
```

### 2. **Configure Your TMA**
- **Course Information**: Fill in your course details
- **Question Structure**: Add questions with their parts and subparts
- **Generate Files**: Click the generate button and download your ZIP file

### 3. **Upload to Overleaf**
- Create a new blank project in Overleaf
- Use the suggested project name from the output
- Delete the default main.tex file
- Upload all files from the downloaded ZIP
- Compile and start writing!

## 📖 Usage Guide

### Course Information Fields

| Field | Description | Example |
|---|---|---|
| **Course Code** | Your module identifier | `M101`, `PHYS201` |
| **TMA Reference** | Assignment number | `01`, `02`, `03`, `04` |
| **Date** | Submission deadline. This is a free format field, any rendition of 'data' may be given e.g. '21 October 2025'. You may retrieve this date later using the '\thedate' command. | `21 January 2026` |
| **Your Name** | Full registered name | `Alex Noel Other` |
| **Student PIN** | Student ID number | `S1234567` |
| **LaTeX Style** | The LaTeX style file to use. This is set to 'ou-tma' and cannot be changed. | `ou-tma` (default) |
| **Base Filename** | Main document name | `TMA` (creates TMA.tex) |

### Question Structure

#### **Marks Field**
- Enter total marks per question as a number
- Examples: `25`, `30`, `15`, `20`
- Total should equal 100 for standard TMAs

#### **Parts Field**
- List question parts separated by commas
- Examples: `a,b,c,d` or `a,b,c,d,e,f`
- Use lowercase letters for consistency

#### **Subparts Field**
- Format: `part:subpart1,subpart2;part2:subpart1,subpart2`
- Examples:
  - `a:i,ii,iii` - Part (a) has subparts (i), (ii), (iii)
  - `a:i,ii;c:1,2,3` - Part (a) has roman numerals, part (c) has numbers
  - Leave blank if no subparts needed

### Example TMA Structure

```
Question 1: Marks=30, Parts=a,b,c, Subparts=a:i,ii,iii;c:i,ii
Question 2: Marks=25, Parts=a,b,c,d, Subparts=b:1,2,3
Question 3: Marks=25, Parts=a,b,c,d, Subparts=(blank)
Question 4: Marks=20, Parts=a,b, Subparts=a:i,ii;b:i,ii,iii
```

### Package Options

| Option | Description |
|---|---|
| **roman** | Use Roman numerals for part numbering (i, ii, iii). If not selected, alphabetic numbering (a, b, c) is used. |
| **cleveref** | Enable cleveref for smart cross-referencing. |
| **pdfbookmark** | Add PDF bookmarks for questions. |
| **legacy** | Enable legacy command definitions (e.g., \vec). |

### Buttons

| Button | Description |
|---|---|
| **Add Question** | Creates a new question entry. |
| **Clear All** | Resets all fields and questions to their default values. |
| **Example** | Populates the form with example questions. |
| **Help** | Shows this help dialog. |
| **Generate TMA Files** | Creates the LaTeX file structure and downloads it as a ZIP file. |
| **Save Settings** | Saves your current configuration to your browser's local storage. |
| **Load Settings** | Loads a previously saved configuration from a .json file. |
| **Export Settings** | Exports your current configuration to a .json file. |
| **Clear Saved Settings** | Deletes your saved settings from your browser's local storage and reloads the application with the default settings. |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+G` | Generate TMA Files |
| `Ctrl+S` | Save Settings |
| `Ctrl+H` | Show Help Dialog |
| `Esc` | Close Help Dialog |

## 🔧 Technical Features

### **Modern JavaScript (ES6+)**
- Modular architecture with clean separation of concerns
- Comprehensive error handling and validation
- Professional code documentation and type hints (via JSDoc)

### **Browser Compatibility**
- **Modern browsers** (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- **Required features**: ES6 modules, LocalStorage, Fetch API, JSZip
- **Optional features**: Service Workers (for offline use)

### **File Generation**
- **Complete LaTeX structure** matching desktop version
- **Professional style files** included (ou-tma.sty)
- **ZIP packaging** with JSZip for easy download
- **Cross-platform compatibility** (Windows, Mac, Linux)

### **Data Privacy**
- **100% client-side** - no data sent to servers
- **Local storage only** - data stays in your browser
- **No tracking** or analytics
- **Open source** - fully transparent

## 📁 Generated File Structure

```
Downloaded ZIP File:
├── TMA.tex              # Main document (compile this)
├── q1.tex               # Question 1 structure
├── q1a.tex              # Question 1 part (a) - EDIT THIS
├── q1b.tex              # Question 1 part (b) - EDIT THIS
├── q2.tex               # Question 2 structure
├── q2a.tex              # Question 2 part (a) - EDIT THIS
├── q1a_0.tex            # Subpart files (if subparts exist)
├── q1a_1.tex            # 
└── ou-tma.sty           # Main LaTeX style file
```

## 🌐 Overleaf Integration

### **Step-by-Step Upload Process**

1. **Generate Files**
   - Configure your TMA in the browser app
   - Click "Generate TMA Files"
   - Download the ZIP file

2. **Create Overleaf Project**
   - Go to [overleaf.com](https://overleaf.com)
   - Create new blank project
   - Use suggested name: `COURSE TMA XX (YEAR)`

3. **Upload Files**
   - Delete default `main.tex` in Overleaf
   - Upload **all files** from downloaded ZIP
   - Overleaf will auto-detect the structure

4. **Compile and Edit**
   - Set `TMA.tex` as main document
   - Click "Recompile" to generate PDF
   - Edit part files (q1a.tex, q1b.tex, etc.) for your answers

### **Overleaf Benefits**
- ✅ **No local LaTeX installation** required
- ✅ **Real-time collaborative editing**
- ✅ **Professional PDF output**
- ✅ **Version history and backup**
- ✅ **Cross-device synchronization**
- ✅ **Rich text editor** with LaTeX support

## 🛠️ Development

### **File Structure**
```
tma-latex-generator/
├── index.html           # Main application
├── styles.css           # Comprehensive styling
├── script.js            # Application logic (1400+ lines)
├── tma.sty              # LaTeX style files
├── tma-extras.sty       #
└── README-BROWSER.md    # This file
```

### **Key JavaScript Modules**
- **CONFIG** - Application configuration and constants
- **State** - Global application state management
- **Utils** - Utility functions and helpers
- **Storage** - Local storage and settings management
- **Tooltip** - Interactive help system
- **Validation** - Input validation and error handling
- **LaTeXGenerator** - File generation engine
- **UI** - User interface management

### **Architecture Highlights**
- **Modular design** with clear separation of concerns
- **Event-driven architecture** with proper cleanup
- **Memory efficient** with debounced operations
- **Error resilient** with comprehensive try-catch blocks
- **Accessibility friendly** with ARIA labels and keyboard navigation

## 🔍 Troubleshooting

### **Common Issues**

**❌ Files not downloading**
- Check if browser blocks pop-ups/downloads
- Try using Chrome/Firefox for best compatibility
- Ensure JavaScript is enabled

**❌ Settings not saving**
- Check if browser supports LocalStorage
- Try clearing browser cache and cookies
- Disable private/incognito mode

**❌ Validation errors**
- Check that total marks equal 100
- Ensure all required fields are filled
- Verify subparts format: `part:sub1,sub2`

**❌ Overleaf upload issues**
- Upload **all files** from the ZIP
- Don't modify file names or structure
- Set TMA.tex as main document
- Check LaTeX compilation errors

### **Browser Requirements**
- **JavaScript**: Must be enabled
- **LocalStorage**: Required for settings
- **Modern browser**: Chrome 60+, Firefox 55+, Safari 12+
- **File downloads**: Must be enabled

## 🆚 Desktop vs Browser Comparison

| Feature | Desktop Version | Browser Version |
|---------|-----------------|-----------------|
| **Installation** | Python required | None required |
| **Platform** | Windows/Mac/Linux | Any with browser |
| **Updates** | Manual download | Always latest |
| **Offline** | Yes | Yes (after first load) |
| **Performance** | Native speed | Near-native |
| **Storage** | File system | Browser storage |
| **Sharing** | File transfer | URL sharing |
| **Accessibility** | Platform-specific | Web standards |

## 📄 License

MIT License - same as the desktop version. See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! The browser version maintains the same high standards as the desktop version:

- **Code quality**: Professional JavaScript with JSDoc documentation
- **User experience**: Intuitive interface with comprehensive help
- **Compatibility**: Cross-browser support for modern browsers
- **Performance**: Optimized for speed and memory efficiency

## 🎓 Educational Impact

This browser version makes the TMA LaTeX Generator accessible to:
- **Students without Python experience**
- **Chromebook and tablet users**
- **Shared/restricted computer environments**
- **Quick one-time users**
- **Mobile device users**

Perfect for academic institutions wanting to provide LaTeX tools without software installation requirements.

---

**🌟 Ready to create professional LaTeX documents? Open `index.html` and start generating!**