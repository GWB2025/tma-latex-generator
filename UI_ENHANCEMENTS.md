# UI Enhancements - TMA LaTeX Generator

## Summary
Added comprehensive tooltips and help system to improve user experience and provide clear guidance on using the application.

## New Features Added

### 1. ToolTip Class
- Custom tooltip implementation that shows helpful information when hovering over widgets
- Automatically positions tooltips near the widget
- Styled with yellow background and border for visibility
- Word wrapping for longer tooltip text

### 2. Comprehensive Tooltips Added

#### Basic Settings Fields:
- **Course Code**: "Your module code (e.g., MATH101, PHYS201, CHEM301)"
- **TMA Reference**: "TMA assignment number (e.g., 01, 02, 03, 04)"
- **Cut-off Date**: "Assignment submission deadline (e.g., '21 January 2026', 'TBD')"
- **Your Name**: "Your full name as registered with your institution"
- **Student PIN**: "Your student identification number (e.g., S1234567)"
- **LaTeX Style**: "LaTeX style file to use (usually 'tma' for academic assignments)"
- **Output Directory**: "Directory where LaTeX files will be created. Use Browse button or type path directly."
- **Base Filename**: "Name for main LaTeX file (usually 'TMA'). Creates TMA.tex as main file."

#### Question Structure Fields:
- **Marks**: "Total marks for this question (e.g., 25, 30, 15)"
- **Parts**: "Question parts separated by commas\nExamples: 'a,b,c,d' or 'a,b' or 'a,b,c,d,e,f'"
- **Subparts**: "Subparts for each part using format: part:sub1,sub2\nExamples:\n'a:i,ii,iii' or 'a:i,ii;c:1,2,3'\nLeave blank if no subparts"

#### Control Buttons:
- **Browse**: "Click to select output directory"
- **Clear All**: "Remove all questions from the structure (cannot be undone!)"
- **Add Question**: "Add a new question to the structure"
- **Help**: "Show comprehensive help with examples and instructions"
- **Remove**: "Remove this question from the structure"
- **Generate TMA Files**: "Create the LaTeX file structure based on your question setup"
- **Save Settings**: "Save your current configuration to avoid re-entering next time"
- **Exit**: "Close the application"

### 3. Help Dialog System

#### Features:
- **Modal dialog** with comprehensive user guide
- **Scrollable content** for easy reading
- **Emoji icons** for visual organisation
- **Centred positioning** on screen
- **Resizable window** for user preference

#### Content Sections:
1. **Overview** - What the application does
2. **Step-by-Step Guide** - Complete walkthrough
3. **Field Explanations** - Detailed field descriptions
4. **Complete Examples** - Real-world usage examples
5. **Common TMA Patterns** - Typical academic assignment structures
6. **Generated Files** - What gets created
7. **Controls** - Button explanations and tips
8. **Troubleshooting** - Common issues and solutions

#### Example Scenarios Covered:
- **Simple Question**: Basic 4-part question without subparts
- **Complex Question**: Mixed parts with different subpart structures
- **Mixed Numbering**: Roman numerals and numbers in different parts
- **Typical Academic TMA**: 4 questions × 25 marks structure

### 4. Enhanced User Experience

#### Improvements:
- **Contextual Help**: Tooltips appear when hovering over any input field or button
- **Instant Guidance**: No need to remember field formats or requirements
- **Error Prevention**: Clear examples help avoid common mistakes
- **Self-Service Support**: Comprehensive help reduces need for external documentation

#### Visual Enhancements:
- Clean, professional tooltip styling
- Consistent tooltip positioning
- Non-intrusive design that doesn't interfere with workflow
- Easy-to-read font and colour scheme

## Testing Results
- ✅ Application launches successfully with all enhancements
- ✅ All tooltips display correctly on hover
- ✅ Help dialog opens and displays comprehensive content
- ✅ All existing functionality preserved
- ✅ File generation works with enhanced UI

## Benefits for Users

### 1. Reduced Learning Curve
- New users can understand field requirements immediately
- Examples provided directly in tooltips
- No need to consult external documentation

### 2. Error Reduction
- Clear format specifications prevent input mistakes
- Examples show correct syntax for complex fields
- Warning tooltips for potentially destructive actions

### 3. Improved Workflow
- Quick access to help without interrupting work
- Context-sensitive guidance when needed
- Comprehensive reference available via Help button

### 4. Better Accessibility
- Visual cues for field requirements
- Consistent help system throughout application
- Self-documenting interface reduces confusion

## Technical Implementation
- Lightweight tooltip system with minimal overhead
- Modal help dialog with proper window management
- Preserved all existing functionality and styling
- Clean, maintainable code structure