# Setup Guide for AI Code Review Application
# #fffbf0

## Prerequisites
1. Python 3.8 or higher installed on your system
2. Git (optional, for cloning the repository)
3. A Google Gemini API key

## Step-by-Step Setup

### 1. Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### 2. Clone/Download the Repository
1. Either clone the repository using Git:
   ```bash
   git clone <repository-url>
   cd AiCodeReview
   ```
   OR
2. Download and extract the ZIP file to your desired location

### 3. Set Up Virtual Environment
1. Open Command Prompt in the project directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` at the start of your command prompt

### 4. Install Dependencies
1. Make sure you're in the virtual environment (you should see `(venv)` in your prompt)
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 5. Configure API Key
1. Create a `.env` file in the project root directory
2. Add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual API key

### 6. Run the Application
1. Make sure your virtual environment is activated
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - If port 5000 is already in use, you can specify a different port:
   ```bash
   python app.py --port 5001
   ```

2. **Module Not Found Errors**
   - Make sure you're in the virtual environment
   - Try reinstalling dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **API Key Issues**
   - Verify your API key is correctly set in the `.env` file
   - Make sure there are no spaces around the equals sign
   - Check that the file is saved with UTF-8 encoding

4. **Python Version Issues**
   - Verify you're using Python 3.8 or higher:
   ```bash
   python --version
   ```

### Required Files
Make sure these files are present in your project directory:
- `app.py`
- `requirements.txt`
- `.env` (with your API key)
- `static/style.css`
- `static/script.js`
- `templates/index.html`

## Development Tips

1. **Using VS Code**
   - Install the Python extension
   - Select the correct Python interpreter (from the virtual environment)
   - Install recommended extensions for Python development

2. **Debugging**
   - The application runs in debug mode by default
   - Changes to Python files will automatically reload the server
   - Check the console for error messages

3. **Browser Developer Tools**
   - Use F12 to open developer tools
   - Check the Console tab for JavaScript errors
   - Use the Network tab to monitor API requests

## Security Notes

1. Never commit your `.env` file to version control
2. Keep your API key secure and don't share it
3. The application is for development use only
4. Don't expose the application to the public internet without proper security measures

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/)
- [Python Virtual Environment Guide](https://docs.python.org/3/tutorial/venv.html) 