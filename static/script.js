document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('codeForm');
    const codeInput = document.getElementById('codeInput');
    const fileUpload = document.getElementById('fileUpload');
    const languageSelect = document.getElementById('languageSelect');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const analysisContent = document.getElementById('analysisContent');
    const error = document.getElementById('error');
    const downloadReport = document.getElementById('downloadReport');

    // Handle language selection
    languageSelect.addEventListener('change', function() {
        codeInput.className = 'language-' + this.value;
        Prism.highlightElement(codeInput);
    });

    // Handle code input and highlight
    codeInput.addEventListener('input', function() {
        Prism.highlightElement(this);
    });

    // Handle file upload
    fileUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                codeInput.textContent = e.target.result;
                // Set language based on file extension
                const extension = file.name.split('.').pop().toLowerCase();
                const languageMap = {
                    'py': 'python',
                    'js': 'javascript',
                    'java': 'java',
                    'cpp': 'cpp',
                    'c': 'c',
                    'h': 'c',
                    'hpp': 'cpp',
                    'cs': 'csharp',
                    'go': 'go',
                    'rs': 'rust',
                    'rb': 'ruby',
                    'php': 'php'
                };
                if (languageMap[extension]) {
                    languageSelect.value = languageMap[extension];
                    codeInput.className = 'language-' + languageMap[extension];
                    Prism.highlightElement(codeInput);
                }
            };
            reader.readAsText(file);
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset UI
        loading.classList.remove('d-none');
        results.classList.add('d-none');
        error.classList.add('d-none');
        
        const formData = new FormData();
        formData.append('code', codeInput.textContent);
        formData.append('language', languageSelect.value);
        
        if (fileUpload.files.length > 0) {
            formData.append('file', fileUpload.files[0]);
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                analysisContent.innerHTML = data.analysis;
                // Highlight code blocks in the analysis
                analysisContent.querySelectorAll('pre code').forEach((block) => {
                    if (!block.className) {
                        block.className = 'language-' + languageSelect.value;
                    }
                    Prism.highlightElement(block);
                });
                results.classList.remove('d-none');
                error.classList.add('d-none');
            } else {
                throw new Error(data.error || 'An error occurred while analyzing the code.');
            }
        } catch (err) {
            error.textContent = err.message;
            error.classList.remove('d-none');
            results.classList.add('d-none');
        } finally {
            loading.classList.add('d-none');
        }
    });

    // Handle report download
    downloadReport.addEventListener('click', function() {
        const content = analysisContent.innerText;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'code-review-report.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });

    // Initial syntax highlighting
    Prism.highlightElement(codeInput);
}); 