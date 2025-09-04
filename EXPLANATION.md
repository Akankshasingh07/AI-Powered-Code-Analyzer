# AI Code Review Application - Technical Documentation

## Overview
This application provides an AI-powered code review service using Google's Gemini API. Users can submit code either by direct input or file upload, and receive detailed analysis covering code quality, potential bugs, performance considerations, style, and security aspects.

## Technical Architecture

### 1. Backend (app.py)
The backend is built with Flask and handles:

#### API Integration
- Uses Google's Gemini API (gemini-2.0-flash model) for code analysis
- Requires a Google API key stored in `.env` file
- Processes code through a structured prompt system

#### Request Handling
- Supports both direct code input and file uploads
- Validates file types and sizes
- Manages temporary file storage and cleanup

#### Response Processing
- Formats AI responses into structured HTML
- Handles markdown-to-HTML conversion
- Implements error handling and response validation

### 2. Frontend

#### HTML Structure (templates/index.html)
- Two-column layout using Bootstrap
- Left column: Code input section
  - Code editor with syntax highlighting
  - Language selector
  - File upload option
- Right column: Analysis results section
  - Formatted analysis output
  - Download report option
- Loading indicators and error messages

#### CSS Styling (static/style.css)
- GitHub-inspired code editor theme
- Responsive design
- Custom scrollbars
- Syntax highlighting colors
- Analysis formatting

#### JavaScript (static/script.js)
- Handles form submissions
- Manages file uploads
- Updates syntax highlighting
- Handles API responses
- Manages UI state
- Implements report downloads

## Key Features

### 1. Code Input
- Syntax-highlighted code editor
- Support for multiple programming languages
- File upload capability
- Auto-language detection from file extensions

### 2. Code Analysis
- Code quality assessment
- Bug detection
- Performance analysis
- Style recommendations
- Security evaluation

### 3. User Interface
- Real-time syntax highlighting
- Loading indicators
- Error handling
- Downloadable reports
- Responsive design

## Implementation Details

### Code Editor
- Uses Prism.js for syntax highlighting
- Supports multiple programming languages
- GitHub-inspired color scheme
- Auto-resizing capability

### Analysis Processing
1. Code submission is processed through Flask
2. Gemini API analyzes the code
3. Response is formatted into structured HTML
4. Results are displayed with proper formatting

### Security Measures
- File size limits (16MB max)
- File type validation
- Input sanitization
- Temporary file cleanup
- API key protection

## Setup and Configuration

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Required Python packages (see requirements.txt)

### Environment Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API key:
   - Create `.env` file
   - Add: `GOOGLE_API_KEY=your_api_key_here`

### Running the Application
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Access the application at `http://localhost:5000`

## File Structure
```
project/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── static/
│   ├── style.css      # CSS styles
│   └── script.js      # Frontend JavaScript
├── templates/
│   └── index.html     # Main HTML template
└── uploads/           # Temporary file storage
```

## Customization

### Adding New Languages
1. Update allowed extensions in app.py
2. Add Prism.js language support in index.html
3. Update language selector in index.html
4. Add language mapping in script.js

### Modifying Analysis
- Adjust the prompt in app.py's analyze_code function
- Update format_analysis function for new response structures
- Modify CSS for new analysis components

### Styling Changes
- Main colors and themes in style.css
- Code editor theme in syntax highlighting section
- Analysis output formatting in analysisContent section

## Error Handling
- File validation errors
- API communication errors
- Response formatting errors
- Server errors
- Client-side validation

## Performance Considerations
- File size limitations
- Response caching (if implemented)
- API rate limiting
- Temporary file management

## Security Notes
- API key protection
- File upload validation
- Input sanitization
- Cross-site scripting prevention
- Temporary file cleanup

## Maintenance
- Regular dependency updates
- API version monitoring
- Error log monitoring
- Performance monitoring
- Security updates

This documentation provides a comprehensive overview of the application's architecture, features, and implementation details. For specific questions or issues, refer to the respective code files or create an issue in the repository. 