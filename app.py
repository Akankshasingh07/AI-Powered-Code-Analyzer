import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import re
import html

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'py', 'js', 'java', 'cpp', 'c', 'h', 'hpp', 'cs', 'go', 'rs', 'rb', 'php'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def format_analysis(text):
    # Split into sections
    sections = re.split(r'(?=\d+\.\s+[A-Za-z])', text)
    formatted_sections = []
    
    for section in sections:
        if not section.strip():
            continue
            
        # Extract section number and title
        match = re.match(r'(\d+)\.\s+([^\n]+)', section)
        if match:
            section_num = match.group(1)
            section_title = match.group(2)
            content = section[match.end():].strip()
            
            # Format the content
            formatted_content = format_section_content(content)
            
            # Add formatted section
            formatted_section = f'<h2>{section_num}. {section_title}</h2>\n{formatted_content}'
            formatted_sections.append(formatted_section)
    
    return '\n'.join(formatted_sections)

def format_section_content(content):
    # Handle code blocks first
    content = re.sub(
        r'```(?:\w+)?\n(.*?)```',
        lambda m: f'<div class="code-block"><pre><code>{html.escape(m.group(1).strip())}</code></pre></div>',
        content,
        flags=re.DOTALL
    )
    
    # Handle bullet points
    lines = content.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append('<p></p>')
            continue
            
        # Check for bullet points
        if line.startswith('- '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            line = f'<li>{format_inline_code(line[2:].strip())}</li>'
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            line = f'<p>{format_inline_code(line)}</p>'
            
        formatted_lines.append(line)
    
    if in_list:
        formatted_lines.append('</ul>')
        
    return '\n'.join(formatted_lines)

def format_inline_code(text):
    # Handle inline code with backticks
    return re.sub(
        r'`([^`]+)`',
        lambda m: f'<code>{html.escape(m.group(1))}</code>',
        text
    )

def analyze_code(code, language):
    prompt = f"""Analyze this {language} code:

1. Code Quality and Best Practices
- Use bullet points starting with a hyphen (-)
- Use single backticks for inline code references like `variable_name`

2. Potential Bugs or Issues
- List potential problems and fixes
- Use bullet points with (-)

3. Performance Considerations
- Discuss efficiency and optimizations
- Use bullet points with (-)

4. Style and Readability
- Analyze code clarity
- Suggest improvements
- Use bullet points with (-)

5. Security Concerns
- List security considerations
- Provide recommendations
- Use bullet points with (-)

6. Corrected Code
```{language}
// Your corrected version of the code with all suggested improvements
```

Code to review:
{code}

Important:
- Start each section with its number (1-6)
- Use hyphens (-) for bullet points
- Use backticks for code terms
- Keep sections clearly separated
- Put corrected code in its own section at the end
- Use proper indentation in code blocks"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Pre-process the text to clean up any remaining markdown
        text = text.replace('**', '').replace('*', '-')
        
        # Extract corrected code section explicitly
        corrected_code_pattern = r'6\.\s*Corrected Code\s*```(?:' + language + r')?\s*\n(.*?)```'
        corrected_code_match = re.search(corrected_code_pattern, text, re.DOTALL)
        
        corrected_code = None
        if corrected_code_match:
            corrected_code = corrected_code_match.group(1).strip()
            # Remove the corrected code section from the text
            text = re.sub(corrected_code_pattern, '', text, flags=re.DOTALL)
        
        # Process sections 1-5
        formatted_sections = []
        
        # Split text into sections using regex
        section_pattern = r'(\d+)\.\s+([^\n]+)\n((?:(?!\n\d+\.).)*)'
        sections = re.finditer(section_pattern, text, re.DOTALL)
        
        for section in sections:
            section_num = section.group(1)
            section_title = section.group(2)
            content = section.group(3).strip()
            
            if 1 <= int(section_num) <= 5:  # Only process sections 1-5
                # Add section header
                formatted_sections.append(f'<h2>{section_title}</h2>')
                
                if content:
                    bullet_points = []
                    paragraphs = []
                    
                    for line in content.split('\n'):
                        line = line.strip()
                        if line:
                            # Format inline code
                            line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
                            
                            if line.startswith('-'):
                                if paragraphs:
                                    formatted_sections.append('<p>' + ' '.join(paragraphs) + '</p>')
                                    paragraphs = []
                                bullet_points.append(f'<li>{line[1:].strip()}</li>')
                            else:
                                if bullet_points:
                                    formatted_sections.append('<ul>' + '\n'.join(bullet_points) + '</ul>')
                                    bullet_points = []
                                paragraphs.append(line)
                    
                    # Add any remaining bullet points or paragraphs
                    if bullet_points:
                        formatted_sections.append('<ul>' + '\n'.join(bullet_points) + '</ul>')
                    if paragraphs:
                        formatted_sections.append('<p>' + ' '.join(paragraphs) + '</p>')
        
        # Add the corrected code section at the end with proper styling
        if corrected_code:
            formatted_sections.append('<div class="section-separator"></div>')
            formatted_sections.append('<h2 class="corrected-code-title">Corrected Code</h2>')
            formatted_sections.append(f'<div class="corrected-code-block"><pre><code class="language-{language}">{html.escape(corrected_code)}</code></pre></div>')
        
        return '\n'.join(formatted_sections)
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        code = None
        language = None
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                with open(filepath, 'r') as f:
                    code = f.read()
                language = filename.rsplit('.', 1)[1].lower()
                os.remove(filepath)  # Clean up uploaded file
        
        # Handle pasted code
        if not code and 'code' in request.form:
            code = request.form['code']
            language = request.form.get('language', 'unknown')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        analysis = analyze_code(code, language)
        return jsonify({'analysis': analysis})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 