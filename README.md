# AI Code Review Application

A web application that provides AI-powered code review using the Google Gemini API. Users can upload code files or paste code directly to receive feedback on code quality, style, and potential improvements.

## Features

- File upload support for multiple programming languages
- Direct code pasting with language selection
- AI-powered code analysis using Google Gemini API
- Modern, responsive UI with Bootstrap
- Downloadable analysis reports
- Error handling and user feedback

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-code-review
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. You can either:
   - Upload a code file using the file upload button
   - Paste your code directly into the text area
   - Select the programming language from the dropdown menu

4. Click "Analyze Code" to receive AI-generated feedback

5. View the analysis results and download the report if needed

## Supported Languages

- Python (.py)
- JavaScript (.js)
- Java (.java)
- C++ (.cpp, .hpp)
- C (.c, .h)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)

## Security Notes

- The application uses environment variables for API key storage
- File uploads are validated for allowed extensions
- Maximum file size is limited to 16MB
- Uploaded files are processed and immediately deleted

## Contributing

Feel free to submit issues and enhancement requests! 