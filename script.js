// TMA LaTeX Generator (Browser Edition) - v2.1 - Marks validation fix applied
/**
 * TMA LaTeX Generator - Browser Edition
 * 
 * Professional LaTeX file structure generator for academic TMA assignments.
 * This JavaScript application provides all the functionality of the desktop version
 * with additional browser-specific features and improved user experience.
 * 
 * @author TMA LaTeX Generator Team
 * @version 2.0.0 (Browser Edition)
 * @licence MIT
 */

// ==================== CONSTANTS & CONFIGURATION ====================

const CONFIG = {
    APP_NAME: 'TMA LaTeX Generator',
    VERSION: '2.0.0',
    DEFAULT_VALUES: {
        course: 'MATH101',
        tma_ref: '04',
        cod: '21 January 2026',
        name: 'Alex Taylor',
        pin: 'S1234567',
        style: 'tma',
        basename: 'TMA'
    },
    STORAGE_KEYS: {
        SETTINGS: 'tma_generator_settings',
        QUESTIONS: 'tma_generator_questions'
    },
    VALIDATION: {
        MAX_QUESTIONS: 10,
        MIN_MARKS: 1,
        MAX_MARKS: 100,
        REQUIRED_FIELDS: ['course', 'tma_ref', 'name', 'pin']
    }
};

// ==================== GLOBAL STATE ====================

const State = {
    questions: [],
    currentConfig: { ...CONFIG.DEFAULT_VALUES },
    isGenerating: false,
    tooltipTimeout: null
};

// ==================== UTILITY FUNCTIONS ====================

/**
 * Utility functions for common operations
 */
const Utils = {
    /**
     * Sanitize text for safe HTML insertion
     */
    sanitizeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Format date for display
     */
    formatDate(date = new Date()) {
        return date.toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    },

    /**
     * Generate unique ID
     */
    generateId() {
        return `q_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    /**
     * Deep clone object
     */
    deepClone(obj) {
        return JSON.parse(JSON.stringify(obj));
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Show notification
     */
    showNotification(message, type = 'info', duration = 3000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${Utils.sanitizeHTML(message)}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Add styles dynamically
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    border-left: 4px solid #007acc;
                    max-width: 400px;
                    animation: slideInUp 0.3s ease;
                }
                .notification-success { border-left-color: #28a745; }
                .notification-error { border-left-color: #dc3545; }
                .notification-warning { border-left-color: #ffc107; }
                .notification-content {
                    display: flex;
                    align-items: flex-start;
                    padding: 16px;
                    gap: 12px;
                }
                .notification-message {
                    flex: 1;
                    font-size: 14px;
                    line-height: 1.4;
                }
                .notification-close {
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #666;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                }
                @keyframes slideInUp {
                    from { transform: translateY(100%); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                @keyframes slideOutDown {
                    from { transform: translateY(0); opacity: 1; }
                    to { transform: translateY(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(styles);
        }

        // Add to DOM
        document.body.appendChild(notification);

        // Add close functionality
        const closeBtn = notification.querySelector('.notification-close');
        const close = () => {
            notification.style.animation = 'slideOutDown 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        };

        closeBtn.addEventListener('click', close);

        // Auto remove
        if (duration > 0) {
            setTimeout(close, duration);
        }

        return notification;
    }
};

// ==================== STORAGE MANAGEMENT ====================

/**
 * Local storage management for settings persistence
 */
const Storage = {
    /**
     * Save settings to localStorage
     */
    saveSettings(settings) {
        try {
            localStorage.setItem(CONFIG.STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
            return true;
        } catch (error) {
            console.warn('Could not save settings:', error);
            return false;
        }
    },

    /**
     * Load settings from localStorage
     */
    loadSettings() {
        try {
            const saved = localStorage.getItem(CONFIG.STORAGE_KEYS.SETTINGS);
            return saved ? JSON.parse(saved) : null;
        } catch (error) {
            console.warn('Could not load settings:', error);
            return null;
        }
    },

    /**
     * Save questions to localStorage
     */
    saveQuestions(questions) {
        try {
            localStorage.setItem(CONFIG.STORAGE_KEYS.QUESTIONS, JSON.stringify(questions));
            return true;
        } catch (error) {
            console.warn('Could not save questions:', error);
            return false;
        }
    },

    /**
     * Load questions from localStorage
     */
    loadQuestions() {
        try {
            const saved = localStorage.getItem(CONFIG.STORAGE_KEYS.QUESTIONS);
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.warn('Could not load questions:', error);
            return [];
        }
    },

    /**
     * Export settings as JSON file
     */
    exportSettings() {
        const data = {
            settings: State.currentConfig,
            questions: State.questions,
            exported: new Date().toISOString(),
            version: CONFIG.VERSION
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `tma-generator-settings-${Utils.formatDate().replace(/\s+/g, '-')}.json`;
        link.click();
        URL.revokeObjectURL(url);
    },

    /**
     * Import settings from JSON file
     */
    async importSettings(file) {
        try {
            const text = await file.text();
            const data = JSON.parse(text);

            if (data.settings && data.questions) {
                State.currentConfig = { ...CONFIG.DEFAULT_VALUES, ...data.settings };
                State.questions = data.questions || [];
                
                UI.updateFormFields();
                UI.renderQuestions();
                
                Utils.showNotification('Settings imported successfully!', 'success');
                return true;
            } else {
                throw new Error('Invalid settings file format');
            }
        } catch (error) {
            Utils.showNotification('Error importing settings: ' + error.message, 'error');
            return false;
        }
    }
};

// ==================== TOOLTIP SYSTEM ====================

/**
 * Tooltip management system
 */
const Tooltip = {
    element: null,

    /**
     * Initialize tooltip system
     */
    init() {
        this.element = document.getElementById('tooltip');
        this.bindEvents();
    },

    /**
     * Bind tooltip events
     */
    bindEvents() {
        document.addEventListener('mouseenter', (e) => {
            if (e.target.dataset.tooltip) {
                this.show(e.target, e.target.dataset.tooltip);
            }
        }, true);

        document.addEventListener('mouseleave', (e) => {
            if (e.target.dataset.tooltip) {
                this.hide();
            }
        }, true);

        document.addEventListener('scroll', () => {
            this.hide();
        });
    },

    /**
     * Show tooltip
     */
    show(target, text) {
        if (!this.element) return;

        this.element.textContent = text;
        this.element.classList.add('show');

        // Position tooltip
        const rect = target.getBoundingClientRect();
        const tooltipRect = this.element.getBoundingClientRect();
        
        let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
        let top = rect.top - tooltipRect.height - 10;

        // Adjust if tooltip goes off screen
        if (left < 10) left = 10;
        if (left + tooltipRect.width > window.innerWidth - 10) {
            left = window.innerWidth - tooltipRect.width - 10;
        }
        if (top < 10) {
            top = rect.bottom + 10;
        }

        this.element.style.left = `${left}px`;
        this.element.style.top = `${top}px`;
    },

    /**
     * Hide tooltip
     */
    hide() {
        if (this.element) {
            this.element.classList.remove('show');
        }
    }
};

// ==================== VALIDATION SYSTEM ====================

/**
 * Input validation and error handling
 */
const Validation = {
    /**
     * Validate course configuration
     */
    validateConfig(config) {
        const errors = [];

        // Check required fields
        CONFIG.VALIDATION.REQUIRED_FIELDS.forEach(field => {
            if (!config[field] || config[field].trim() === '') {
                errors.push(`${field.toUpperCase().replace('_', ' ')} is required`);
            }
        });

        // Validate TMA reference format
        if (config.tma_ref && !/^\d{1,2}$/.test(config.tma_ref.trim())) {
            errors.push('TMA Reference should be a number (e.g., 01, 02, 03, 04)');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    },

    /**
     * Validate questions structure
     */
    validateQuestions(questions) {
        const errors = [];
        const warnings = [];
        let totalMarks = 0;

        if (questions.length === 0) {
            errors.push('At least one question is required');
            return { isValid: false, errors, warnings, totalMarks };
        }

        questions.forEach((question, index) => {
            const qNum = index + 1;

            // Validate marks
            const marks = parseInt(question.marks) || 0;
            if (marks < CONFIG.VALIDATION.MIN_MARKS || marks > CONFIG.VALIDATION.MAX_MARKS) {
                errors.push(`Question ${qNum}: Marks must be between ${CONFIG.VALIDATION.MIN_MARKS} and ${CONFIG.VALIDATION.MAX_MARKS}`);
            } else {
                totalMarks += marks;
            }

            // Validate parts
            const parts = question.parts.split(',').map(p => p.trim()).filter(p => p);
            if (parts.length === 0) {
                errors.push(`Question ${qNum}: At least one part is required (e.g., 'a,b,c,d')`);
            }

            // Check for duplicate parts
            const uniqueParts = [...new Set(parts.map(p => p.toLowerCase()))];
            if (parts.length !== uniqueParts.length) {
                errors.push(`Question ${qNum}: Duplicate parts found`);
            }

            // Validate subparts format
            if (question.subparts.trim()) {
                const subpartErrors = this.validateSubparts(question.subparts, parts, qNum);
                errors.push(...subpartErrors);
            }
        });

        // Check total marks - now as warning instead of error
        if (totalMarks !== 100) {
            warnings.push(`Total marks should equal 100 (currently: ${totalMarks})`);
        }

        return {
            isValid: errors.length === 0,
            errors,
            warnings,
            totalMarks
        };
    },

    /**
     * Validate subparts format
     */
    validateSubparts(subpartsText, validParts, questionNum) {
        const errors = [];
        const validPartsLower = validParts.map(p => p.toLowerCase());

        try {
            const subpartGroups = subpartsText.split(';');
            
            subpartGroups.forEach(group => {
                if (!group.includes(':')) {
                    errors.push(`Question ${questionNum}: Invalid subparts format. Use 'part:sub1,sub2' format`);
                    return;
                }

                const [part, subparts] = group.split(':', 2);
                const partName = part.trim().toLowerCase();
                
                if (!validPartsLower.includes(partName)) {
                    errors.push(`Question ${questionNum}: Subpart references invalid part '${part.trim()}'`);
                }

                const subList = subparts.split(',').map(s => s.trim()).filter(s => s);
                if (subList.length === 0) {
                    errors.push(`Question ${questionNum}: Part '${part.trim()}' has no subparts specified`);
                }
            });
        } catch (error) {
            errors.push(`Question ${questionNum}: Invalid subparts format`);
        }

        return errors;
    },

    /**
     * Show validation errors
     */
    showErrors(errors) {
        const errorMessage = errors.join('\n• ');
        Utils.showNotification(`Validation Errors:\n• ${errorMessage}`, 'error', 8000);
    },

    /**
     * Show validation warnings
     */
    showWarnings(warnings) {
        const warningMessage = warnings.join('\n• ');
        Utils.showNotification(`Validation Warnings:\n• ${warningMessage}\n\nYou can continue with generation if needed.`, 'warning', 8000);
    }
};

// ==================== LATEX GENERATION ====================

/**
 * LaTeX file generation system
 */
const LaTeXGenerator = {
    /**
     * Generate main LaTeX document content
     */
    generateMainTex(config, questions) {
        const lines = [
            `% File: ${config.basename}.tex`,
            '% This is the MAIN document file - DO NOT EDIT!',
            '% This file is auto-generated and controls the overall document structure.',
            '% To add your answers, edit the individual question part files (e.g., q1a.tex, q1b.tex)',
// Generated by TMA LaTeX Generator (Browser Edition) - v2.1 (Marks validation fix)
            '',
            `\\documentclass[a4paper,12pt]{article}`,
            `\\usepackage{${config.style}}`,
            `\\myname{${config.name}}`,
            `\\mypin{${config.pin}}`,
            `\\mycourse{${config.course}}`,
            `\\mytma{${config.tma_ref}}`,
            `\\mycod{${config.cod}}`,
            '',
            `\\includeonly{${questions.map((_, i) => `q${i + 1}`).join(',')}}`,
            '',
            '\\begin{document}',
            ...questions.map((_, i) => `\\include{q${i + 1}}`),
            '\\end{document}'
        ];

        return lines.join('\n');
    },

    /**
     * Generate question file content
     */
    generateQuestionTex(config, questionIndex, parts) {
        const qNum = questionIndex + 1;
        const lines = [
            `% !TeX root = ./${config.basename}.tex`,
            `% File: q${qNum}.tex`,
            '% This is a STRUCTURE file - DO NOT EDIT!',
            '% This file controls the layout of question parts.',
            `% To add your answers, edit the individual part files (q${qNum}a.tex, q${qNum}b.tex, etc.)`,
            '% Generated by TMA LaTeX Generator (Browser Edition)',
            '',
            '\\begin{question}',
            ...parts.map(part => [
                `\\qpart %(${part})`,
                `\\input{q${qNum}${part}}`
            ]).flat(),
            '\\end{question}'
        ];

        return lines.join('\n');
    },

    /**
     * Generate part file content
     */
    generatePartTex(config, questionIndex, part) {
        const qNum = questionIndex + 1;
        const lines = [
            `% !TeX root = ./${config.basename}.tex`,
            `% File: q${qNum}${part}.tex`,
            '% This is an ANSWER file - EDIT THIS!',
            `% Add your answer for Question ${qNum} part (${part}) below.`,
            '% You can use LaTeX commands, equations, figures, etc.',
            '% Generated by TMA LaTeX Generator (Browser Edition)',
            '',
            '% Add your answer here:',
            ''
        ];

        return lines.join('\n');
    },

    /**
     * Generate subpart files content
     */
    generateSubpartTex(config, questionIndex, part, subpartIndex) {
        const qNum = questionIndex + 1;
        const lines = [
            `% !TeX root = ./${config.basename}.tex`,
            `% File: q${qNum}${part}_${subpartIndex}.tex`,
            '% This is a SUBPART ANSWER file - EDIT THIS!',
            `% Add your answer for subpart ${subpartIndex + 1} here.`,
            '% You can use LaTeX commands, equations, figures, etc.',
            '% Generated by TMA LaTeX Generator (Browser Edition)',
            '',
            '% Add your answer here:',
            ''
        ];

        return lines.join('\n');
    },

    /**
     * Parse subparts string into structured data
     */
    parseSubparts(subpartsText) {
        const subparts = {};
        
        if (!subpartsText.trim()) return subparts;

        try {
            const groups = subpartsText.split(';');
            groups.forEach(group => {
                const [part, subs] = group.split(':', 2);
                if (part && subs) {
                    const subList = subs.split(',').map(s => s.trim()).filter(s => s);
                    if (subList.length > 0) {
                        subparts[part.trim()] = subList;
                    }
                }
            });
        } catch (error) {
            console.warn('Error parsing subparts:', error);
        }

        return subparts;
    },

    /**
     * Generate all files for download
     */
    async generateFiles(config, questions) {
        const files = new Map();

        // Generate main file
        files.set(`${config.basename}.tex`, this.generateMainTex(config, questions));

        // Generate question and part files
        questions.forEach((question, qIndex) => {
            const parts = question.parts.split(',').map(p => p.trim()).filter(p => p);
            const subparts = this.parseSubparts(question.subparts);

            // Question file
            files.set(`q${qIndex + 1}.tex`, this.generateQuestionTex(config, qIndex, parts));

            // Part files
            parts.forEach(part => {
                files.set(`q${qIndex + 1}${part}.tex`, this.generatePartTex(config, qIndex, part));

                // Subpart files
                if (subparts[part]) {
                    const subpartContent = [
                        '',
                        ...subparts[part].map((_, subIndex) => [
                            '\\qsubpart',
                            `\\input{q${qIndex + 1}${part}_${subIndex}}`
                        ]).flat()
                    ];

                    // Append subparts to part file
                    const partContent = files.get(`q${qIndex + 1}${part}.tex`);
                    files.set(`q${qIndex + 1}${part}.tex`, partContent + subpartContent.join('\n'));

                    // Create individual subpart files
                    subparts[part].forEach((_, subIndex) => {
                        files.set(
                            `q${qIndex + 1}${part}_${subIndex}.tex`,
                            this.generateSubpartTex(config, qIndex, part, subIndex)
                        );
                    });
                }
            });
        });

        // Add style files
        try {
            const tmaStyle = await fetch('./tma.sty').then(r => r.text());
            const tmaExtrasStyle = await fetch('./tma-extras.sty').then(r => r.text());
            files.set('tma.sty', tmaStyle);
            files.set('tma-extras.sty', tmaExtrasStyle);
        } catch (error) {
            console.warn('Could not load style files:', error);
            // Fallback: Generate basic style file content
            files.set('tma.sty', this.generateFallbackStyle());
            files.set('tma-extras.sty', '% TMA Extras style file\n\\endinput');
        }

        return files;
    },

    /**
     * Generate fallback style file if external files are not available
     */
    generateFallbackStyle() {
        return `%% File: tma.sty
%% Basic TMA style file
\\NeedsTeXFormat{LaTeX2e}
\\ProvidesPackage{tma}[2025/09/27 tma package]

% Basic packages
\\RequirePackage{fancyhdr}
\\RequirePackage{amsmath,amssymb}
\\RequirePackage{geometry}

% Geometry settings
\\geometry{
    headheight=10mm,
    headsep=5mm,
    bottom=25mm,
    footskip=15mm,
    lmargin=30mm,
    rmargin=5mm
}

% Question counters
\\newcounter{question}
\\newcounter{qpart}[question]
\\newcounter{qsubpart}[qpart]

% User information commands
\\newcommand{\\name}{\\relax}
\\newcommand{\\tma}{\\relax}
\\newcommand{\\course}{\\relax}
\\newcommand{\\pin}{\\relax}
\\newcommand{\\cod}{\\relax}

\\newcommand{\\myname}[1]{\\renewcommand{\\name}{#1}}
\\newcommand{\\mytma}[1]{\\renewcommand{\\tma}{#1}}
\\newcommand{\\mycourse}[1]{\\renewcommand{\\course}{#1}}
\\newcommand{\\mypin}[1]{\\renewcommand{\\pin}{#1}}
\\newcommand{\\mycod}[1]{\\renewcommand{\\cod}{#1}}

% Question environment
\\newenvironment{question}[1][0]{%
    \\stepcounter{question}%
    \\makebox[0pt][r]{\\large{Q \\thequestion .\\quad}}\\par%
    \\setcounter{page}{1}%
}{%
    \\par \\vspace{3em}%
}

\\newcommand{\\qpart}[1][0]{%
    \\stepcounter{qpart}\\par%
    \\makebox[0pt][r]{\\large{(\\alph{qpart})\\quad}}%
}

\\newcommand{\\qsubpart}[1][0]{%
    \\stepcounter{qsubpart}\\par%
    \\makebox[0pt][r]{\\large{(\\roman{qsubpart})\\quad}}%
}

% Page style
\\pagestyle{fancy}
\\lhead{\\textrm{\\name\\ \\pin}}
\\chead{\\textrm{\\course\\ TMA-\\tma}}
\\rhead{\\textrm{Due: \\cod}}

\\endinput`;
    }
};

// ==================== UI MANAGEMENT ====================

/**
 * User interface management
 */
const UI = {
    elements: {},

    /**
     * Initialize UI elements and event handlers
     */
    init() {
        this.cacheElements();
        this.bindEvents();
        this.loadInitialData();
        this.addInitialQuestion();
    },

    /**
     * Cache DOM elements
     */
    cacheElements() {
        this.elements = {
            // Form elements
            course: document.getElementById('course'),
            tma_ref: document.getElementById('tma_ref'),
            cod: document.getElementById('cod'),
            name: document.getElementById('name'),
            pin: document.getElementById('pin'),
            style: document.getElementById('style'),
            basename: document.getElementById('basename'),

            // Control buttons
            addQuestion: document.getElementById('add-question'),
            clearQuestions: document.getElementById('clear-questions'),
            showHelp: document.getElementById('show-help'),
            generateFiles: document.getElementById('generate-files'),
            saveSettings: document.getElementById('save-settings'),
            loadSettings: document.getElementById('load-settings'),

            // Containers
            questionsContainer: document.getElementById('questions-container'),
            outputText: document.getElementById('output-text'),

            // Modal elements
            helpModal: document.getElementById('help-modal'),
            helpContent: document.getElementById('help-content'),
            closeHelp: document.getElementById('close-help'),
            closeHelpFooter: document.getElementById('close-help-footer'),

            // Loading overlay
            loadingOverlay: document.getElementById('loading-overlay')
        };
    },

    /**
     * Bind event handlers
     */
    bindEvents() {
        // Form changes
        Object.keys(this.elements).forEach(key => {
            if (['course', 'tma_ref', 'cod', 'name', 'pin', 'style', 'basename'].includes(key)) {
                this.elements[key].addEventListener('input', Utils.debounce(() => {
                    this.updateConfig();
                }, 500));
            }
        });

        // Control buttons
        this.elements.addQuestion.addEventListener('click', () => this.addQuestion());
        this.elements.clearQuestions.addEventListener('click', () => this.clearAllQuestions());
        this.elements.showHelp.addEventListener('click', () => this.showHelp());
        this.elements.generateFiles.addEventListener('click', () => this.generateFiles());
        this.elements.saveSettings.addEventListener('click', () => this.saveSettings());
        this.elements.loadSettings.addEventListener('click', () => this.loadSettings());

        // Modal events
        this.elements.closeHelp.addEventListener('click', () => this.hideHelp());
        this.elements.closeHelpFooter.addEventListener('click', () => this.hideHelp());

        // Click outside modal to close
        this.elements.helpModal.addEventListener('click', (e) => {
            if (e.target === this.elements.helpModal) {
                this.hideHelp();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 's':
                        e.preventDefault();
                        this.saveSettings();
                        break;
                    case 'g':
                        e.preventDefault();
                        this.generateFiles();
                        break;
                    case 'h':
                        e.preventDefault();
                        this.showHelp();
                        break;
                }
            }
            if (e.key === 'Escape') {
                this.hideHelp();
            }
        });

        // Auto-save functionality
        setInterval(() => {
            this.autoSave();
        }, 30000); // Auto-save every 30 seconds
    },

    /**
     * Load initial data
     */
    loadInitialData() {
        // Load saved settings
        const savedSettings = Storage.loadSettings();
        if (savedSettings) {
            State.currentConfig = { ...CONFIG.DEFAULT_VALUES, ...savedSettings };
            this.updateFormFields();
        }

        // Load saved questions
        const savedQuestions = Storage.loadQuestions();
        if (savedQuestions.length > 0) {
            State.questions = savedQuestions;
            this.renderQuestions();
        }
    },

    /**
     * Update form fields from current config
     */
    updateFormFields() {
        Object.keys(State.currentConfig).forEach(key => {
            if (this.elements[key]) {
                this.elements[key].value = State.currentConfig[key];
            }
        });
    },

    /**
     * Update config from form fields
     */
    updateConfig() {
        Object.keys(this.elements).forEach(key => {
            if (['course', 'tma_ref', 'cod', 'name', 'pin', 'style', 'basename'].includes(key)) {
                State.currentConfig[key] = this.elements[key].value;
            }
        });
    },

    /**
     * Add initial question if none exist
     */
    addInitialQuestion() {
        if (State.questions.length === 0) {
            this.addQuestion();
        }
    },

    /**
     * Add new question
     */
    addQuestion() {
        if (State.questions.length >= CONFIG.VALIDATION.MAX_QUESTIONS) {
            Utils.showNotification(`Maximum of ${CONFIG.VALIDATION.MAX_QUESTIONS} questions allowed`, 'warning');
            return;
        }

        const question = {
            id: Utils.generateId(),
            marks: '25',
            parts: 'a,b,c,d',
            subparts: ''
        };

        State.questions.push(question);
        this.renderQuestion(question, State.questions.length - 1);
        this.updateQuestionsDisplay();
    },

    /**
     * Remove question
     */
    removeQuestion(questionId) {
        State.questions = State.questions.filter(q => q.id !== questionId);
        this.renderQuestions();
        this.updateQuestionsDisplay();
    },

    /**
     * Clear all questions
     */
    clearAllQuestions() {
        if (State.questions.length === 0) return;

        if (confirm('Are you sure you want to remove all questions? This cannot be undone.')) {
            State.questions = [];
            this.renderQuestions();
            this.updateQuestionsDisplay();
            this.addInitialQuestion(); // Add one question back
        }
    },

    /**
     * Render all questions
     */
    renderQuestions() {
        this.elements.questionsContainer.innerHTML = '';
        State.questions.forEach((question, index) => {
            this.renderQuestion(question, index);
        });
        this.updateQuestionsDisplay();
    },

    /**
     * Render single question
     */
    renderQuestion(question, index) {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-card';
        questionDiv.dataset.questionId = question.id;

        questionDiv.innerHTML = `
            <div class="question-header">
                <h3 class="question-title">Question ${index + 1}</h3>
                <button type="button" class="btn btn-danger btn-small remove-question">
                    🗑️ Remove
                </button>
            </div>
            <div class="question-fields">
                <label>Marks:</label>
                <input type="number" class="question-marks" value="${question.marks}" min="1" max="100"
                       data-tooltip="Total marks for this question (e.g., 25, 30, 15)">
                
                <label>Parts:</label>
                <input type="text" class="question-parts" value="${question.parts}"
                       data-tooltip="Question parts separated by commas (e.g., 'a,b,c,d' or 'a,b')">
                
                <label>Subparts:</label>
                <input type="text" class="question-subparts" value="${question.subparts}"
                       data-tooltip="Subparts format: 'part:sub1,sub2;part2:sub1,sub2' (leave blank if no subparts)">
            </div>
        `;

        this.elements.questionsContainer.appendChild(questionDiv);

        // Bind events for this question
        const removeBtn = questionDiv.querySelector('.remove-question');
        const marksInput = questionDiv.querySelector('.question-marks');
        const partsInput = questionDiv.querySelector('.question-parts');
        const subpartsInput = questionDiv.querySelector('.question-subparts');

        removeBtn.addEventListener('click', () => {
            if (State.questions.length === 1) {
                Utils.showNotification('At least one question is required', 'warning');
                return;
            }
            this.removeQuestion(question.id);
        });

        const updateQuestion = Utils.debounce(() => {
            const questionIndex = State.questions.findIndex(q => q.id === question.id);
            if (questionIndex !== -1) {
                State.questions[questionIndex].marks = marksInput.value;
                State.questions[questionIndex].parts = partsInput.value;
                State.questions[questionIndex].subparts = subpartsInput.value;
            }
        }, 500);

        marksInput.addEventListener('input', updateQuestion);
        partsInput.addEventListener('input', updateQuestion);
        subpartsInput.addEventListener('input', updateQuestion);
    },

    /**
     * Update questions display info
     */
    updateQuestionsDisplay() {
        const totalMarks = State.questions.reduce((sum, q) => sum + (parseInt(q.marks) || 0), 0);
        const questionCount = State.questions.length;

        // Update container header info
        const container = this.elements.questionsContainer;
        let infoDiv = container.querySelector('.questions-info');
        
        if (!infoDiv) {
            infoDiv = document.createElement('div');
            infoDiv.className = 'questions-info';
            container.insertBefore(infoDiv, container.firstChild);
        }

        const marksColor = totalMarks === 100 ? '#28a745' : totalMarks > 100 ? '#dc3545' : '#ffc107';
        infoDiv.innerHTML = `
            <div style="text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin-bottom: 16px;">
                <strong>Questions: ${questionCount}</strong> | 
                <strong style="color: ${marksColor}">Total Marks: ${totalMarks}/100</strong>
                ${totalMarks !== 100 ? ' ⚠️' : ' ✅'}
            </div>
        `;
    },

    /**
     * Show help modal
     */
    showHelp() {
        this.elements.helpContent.innerHTML = this.getHelpContent();
        this.elements.helpModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    },

    /**
     * Hide help modal
     */
    hideHelp() {
        this.elements.helpModal.classList.remove('show');
        document.body.style.overflow = '';
    },

    /**
     * Get comprehensive help content
     */
    getHelpContent() {
        return `
            <div class="help-content">
                <h3>🎯 Overview</h3>
                <p>The TMA LaTeX Generator creates structured LaTeX files for academic assignments, specifically designed for Overleaf. You manually specify the question structure, and the application generates all necessary files organised for easy editing and upload to Overleaf.</p>

                <h3>📋 Step-by-Step Guide</h3>
                
                <h4>1. Course Information</h4>
                <ul>
                    <li><strong>Course Code:</strong> Your module code (e.g., MATH101, PHYS201)</li>
                    <li><strong>TMA Reference:</strong> Assignment number (e.g., 01, 02, 03, 04)</li>
                    <li><strong>Cut-off Date:</strong> Submission deadline (e.g., "21 January 2026")</li>
                    <li><strong>Your Name:</strong> Your full name as registered</li>
                    <li><strong>Student PIN:</strong> Your student identification number</li>
                    <li><strong>LaTeX Style:</strong> Style file to use (usually "tma")</li>
                    <li><strong>Base Filename:</strong> Main file name (usually "TMA")</li>
                </ul>

                <h4>2. Question Structure</h4>
                <p>This is where you specify how your TMA is organised:</p>
                
                <h5>📝 Marks Field</h5>
                <p>Enter the total marks for each question as a number.<br>
                Examples: 25, 30, 15, 20</p>

                <h5>📝 Parts Field</h5>
                <p>List question parts separated by commas.<br>
                Examples:</p>
                <ul>
                    <li>"a,b,c,d" - for parts (a), (b), (c), (d)</li>
                    <li>"a,b" - for just parts (a), (b)</li>
                    <li>"a,b,c,d,e,f" - for six parts</li>
                </ul>

                <h5>📝 Subparts Field</h5>
                <p>Specify subparts for each part using the format: part:subparts<br>
                Multiple parts separated by semicolons.<br>
                Examples:</p>
                <ul>
                    <li>"a:i,ii,iii" - part (a) has subparts (i), (ii), (iii)</li>
                    <li>"a:i,ii;c:i,ii,iii,iv" - part (a) has 2 subparts, part (c) has 4</li>
                    <li>"b:1,2,3" - part (b) has numbered subparts (1), (2), (3)</li>
                    <li>Leave blank if no subparts needed</li>
                </ul>

                <h4>3. Complete Examples</h4>
                
                <h5>📚 Example 1: Simple Question</h5>
                <p>Question 1: Marks=25, Parts=a,b,c,d, Subparts=(blank)<br>
                Creates: Q1 with parts (a), (b), (c), (d), no subparts</p>

                <h5>📚 Example 2: Complex Question</h5>
                <p>Question 1: Marks=30, Parts=a,b,c, Subparts=a:i,ii,iii;c:i,ii<br>
                Creates:</p>
                <ul>
                    <li>Q1(a) with subparts (i), (ii), (iii)</li>
                    <li>Q1(b) with no subparts</li>
                    <li>Q1(c) with subparts (i), (ii)</li>
                </ul>

                <h4>4. Generated Files</h4>
                <p>The application creates:</p>
                <ul>
                    <li>Main LaTeX file (TMA.tex)</li>
                    <li>Question files (q1.tex, q2.tex, etc.)</li>
                    <li>Part files (q1a.tex, q1b.tex, etc.)</li>
                    <li>Subpart files (q1a_0.tex, q1a_1.tex, etc.)</li>
                    <li>Style files (tma.sty, tma-extras.sty)</li>
                </ul>

                <h4>5. Keyboard Shortcuts</h4>
                <ul>
                    <li><kbd>Ctrl+G</kbd> - Generate Files</li>
                    <li><kbd>Ctrl+S</kbd> - Save Settings</li>
                    <li><kbd>Ctrl+H</kbd> - Show Help</li>
                    <li><kbd>Esc</kbd> - Close Help</li>
                </ul>

                <h4>6. Using with Overleaf</h4>
                <p>This tool generates files specifically for Overleaf:</p>
                <ol>
                    <li>Generate your TMA files using this browser app</li>
                    <li>Download the ZIP file containing all LaTeX files</li>
                    <li>Go to overleaf.com and create a new blank project</li>
                    <li>Use the suggested project name from the output</li>
                    <li>Delete the default main.tex file in Overleaf</li>
                    <li>Upload all files from the downloaded ZIP</li>
                    <li>Set TMA.tex as the main document and compile</li>
                    <li>Start editing individual part files (q1a.tex, q1b.tex, etc.)</li>
                </ol>

                <h3>💡 Tips</h3>
                <ul>
                    <li>Settings are automatically saved as you type</li>
                    <li>Total marks typically equal 100 for most TMAs, but this isn't always required</li>
                    <li>If marks don't total 100, you'll see a warning but can still generate files</li>
                    <li>Use consistent part naming (lowercase: a,b,c)</li>
                    <li>Test with simple structures first</li>
                    <li>The app works entirely in your browser - no data is sent to servers</li>
                </ul>
            </div>
        `;
    },

    /**
     * Save current settings
     */
    saveSettings() {
        this.updateConfig();
        
        const saved = Storage.saveSettings(State.currentConfig) && Storage.saveQuestions(State.questions);
        
        if (saved) {
            Utils.showNotification('Settings saved successfully!', 'success');
        } else {
            Utils.showNotification('Could not save settings. Please try again.', 'error');
        }
    },

    /**
     * Load settings from file
     */
    loadSettings() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (file) {
                await Storage.importSettings(file);
            }
        };
        input.click();
    },

    /**
     * Auto-save functionality
     */
    autoSave() {
        if (State.questions.length > 0 || Object.keys(State.currentConfig).length > 0) {
            this.updateConfig();
            Storage.saveSettings(State.currentConfig);
            Storage.saveQuestions(State.questions);
        }
    },

    /**
     * Generate and download files
     */
    async generateFiles() {
        if (State.isGenerating) return;

        State.isGenerating = true;
        this.showLoading();
        this.updateConfig();

        try {
            // Validate configuration
            const configValidation = Validation.validateConfig(State.currentConfig);
            if (!configValidation.isValid) {
                Validation.showErrors(configValidation.errors);
                return;
            }

            // Validate questions
            const questionsValidation = Validation.validateQuestions(State.questions);
            if (!questionsValidation.isValid) {
                Validation.showErrors(questionsValidation.errors);
                return;
            }

            // Show warnings but allow continuation
            if (questionsValidation.warnings && questionsValidation.warnings.length > 0) {
                Validation.showWarnings(questionsValidation.warnings);
                // Small delay to ensure warning is visible before download dialog
                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            // Generate output log
            this.updateOutput('Generating TMA files...\n\n');
            this.updateOutput('Configuration:\n');
            this.updateOutput(`Course: ${State.currentConfig.course}\n`);
            this.updateOutput(`TMA: ${State.currentConfig.tma_ref}\n`);
            this.updateOutput(`Name: ${State.currentConfig.name}\n`);
            this.updateOutput(`Due: ${State.currentConfig.cod}\n\n`);

            this.updateOutput('Question Structure:\n');
            State.questions.forEach((question, index) => {
                this.updateOutput(`Q${index + 1}: ${question.marks} marks, Parts: ${question.parts}\n`);
                if (question.subparts) {
                    this.updateOutput(`    Subparts: ${question.subparts}\n`);
                }
            });

            this.updateOutput(`\nTotal Marks: ${questionsValidation.totalMarks}/100\n\n`);

            // Generate LaTeX files
            this.updateOutput('Generating LaTeX files...\n');
            const files = await LaTeXGenerator.generateFiles(State.currentConfig, State.questions);

            // Create ZIP file
            this.updateOutput('Creating download package...\n');
            const zip = new JSZip();
            
            for (const [filename, content] of files) {
                zip.file(filename, content);
            }

            const blob = await zip.generateAsync({ type: 'blob' });
            
            // Generate suggested project name
            const projectName = this.generateOverleafProjectName();

            // Download file
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${State.currentConfig.course}-TMA${State.currentConfig.tma_ref}-LaTeX-Files.zip`;
            link.click();
            URL.revokeObjectURL(url);

            // Show success output
            this.updateOutput('\n=== GENERATION COMPLETE ===\n');
            this.updateOutput('✅ TMA files generated successfully!\n\n');
            this.updateOutput('📁 Files created:\n');
            for (const filename of files.keys()) {
                this.updateOutput(`  • ${filename}\n`);
            }

            this.updateOutput('\n🌐 OVERLEAF SETUP:\n');
            this.updateOutput('Suggested project name:\n');
            this.updateOutput(`  "${projectName}"\n\n`);
            this.updateOutput('Next steps:\n');
            this.updateOutput('1. Go to overleaf.com and sign in\n');
            this.updateOutput('2. Create new blank project with suggested name\n');
            this.updateOutput('3. Delete default main.tex in Overleaf\n');
            this.updateOutput('4. Upload ALL files from downloaded ZIP\n');
            this.updateOutput('5. Compile and start editing!\n\n');
            this.updateOutput('📝 Edit the part files (q1a.tex, q1b.tex, etc.) for your answers.\n');
            this.updateOutput('🚀 Your LaTeX structure is ready for professional academic writing!\n');

            // Save settings after successful generation
            this.saveSettings();

            Utils.showNotification('TMA files generated and downloaded successfully!', 'success');

        } catch (error) {
            console.error('Generation error:', error);
            this.updateOutput(`\n❌ Error: ${error.message}\n`);
            Utils.showNotification('Error generating files: ' + error.message, 'error');
        } finally {
            State.isGenerating = false;
            this.hideLoading();
        }
    },

    /**
     * Generate suggested Overleaf project name
     */
    generateOverleafProjectName() {
        const course = State.currentConfig.course.toUpperCase();
        const tmaRef = State.currentConfig.tma_ref.padStart(2, '0');
        const year = new Date().getFullYear();
        
        // Try to extract year from cut-off date
        const codMatch = State.currentConfig.cod.match(/\b(20\d{2})\b/);
        const actualYear = codMatch ? codMatch[1] : year;

        return `${course} TMA ${tmaRef} (${actualYear})`;
    },

    /**
     * Show loading overlay
     */
    showLoading() {
        this.elements.loadingOverlay.classList.add('show');
    },

    /**
     * Hide loading overlay
     */
    hideLoading() {
        this.elements.loadingOverlay.classList.remove('show');
    },

    /**
     * Update output text
     */
    updateOutput(text) {
        this.elements.outputText.textContent += text;
        this.elements.outputText.scrollTop = this.elements.outputText.scrollHeight;
    },

    /**
     * Clear output text
     */
    clearOutput() {
        this.elements.outputText.textContent = '';
    }
};

// ==================== APPLICATION INITIALIZATION ====================

/**
 * Initialize the application when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 TMA LaTeX Generator - Browser Edition starting...');
    
    try {
        // Initialize all systems
        Tooltip.init();
        UI.init();
        
        console.log('✅ Application initialized successfully');
        
        // Show welcome message
        setTimeout(() => {
            Utils.showNotification('Welcome to TMA LaTeX Generator! 🎓\nYour settings are automatically saved as you work.', 'success', 5000);
        }, 1000);
        
    } catch (error) {
        console.error('❌ Application initialization failed:', error);
        Utils.showNotification('Application failed to initialize. Please refresh the page.', 'error', 10000);
    }
});

// Export for debugging (if needed)
if (typeof window !== 'undefined') {
    window.TMAGenerator = {
        State,
        Config: CONFIG,
        Utils,
        Storage,
        Validation,
        LaTeXGenerator,
        UI
    };
}