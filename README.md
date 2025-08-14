# Spec2Test Lite

An AI-powered tool that automatically generates test cases from software requirements documents (PDF/DOCX).

**Created by Jeremie Nombro**

## Features

- 📄 **Multi-format Support**: Upload PDF or DOCX requirement documents
- 🤖 **AI-Powered**: Uses local LLM (Ollama) to extract test cases
- 📊 **CSV Export**: Download generated test cases as CSV files
- 🚀 **Simple Interface**: Clean Streamlit web interface
- ⚡ **Fast Processing**: Efficient text chunking and processing

## Quick Start

### Prerequisites

1. **Install Ollama** (for local LLM):

   ```bash
   # Visit https://ollama.ai for installation instructions
   # Then pull a model:
   ollama pull llama3
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Quick Start (Recommended)**

```bash
python launch.py
```

**Option 2: Manual Start**

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## Usage

1. **Upload Document**: Click "Browse files" and select your PDF or DOCX requirements document
2. **Process**: The app will automatically chunk and process your document
3. **Review**: View generated test cases in the data table
4. **Download**: Click "Download CSV" to save your test cases

## Project Structure

```
spec2test-lite/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── core/
│   ├── parser.py            # Document parsing (PDF/DOCX)
│   ├── chunker.py           # Text chunking logic
│   ├── prompt.py            # LLM prompt templates
│   └── generator.py         # LLM interaction & output parsing
└── utils/
    └── file_utils.py        # File handling utilities
```

## Configuration

All configuration settings are in `config/settings.py`:

### Model Settings

- `DEFAULT_MODEL`: LLM model to use (default: "llama3")
- `CHUNK_SIZE`: Maximum characters per text chunk (default: 1000)
- `TIMEOUT_SECONDS`: LLM request timeout (default: 60)

### File Processing

- `SUPPORTED_FORMATS`: List of supported file extensions
- `TEMP_FILE_PREFIX`: Prefix for temporary files

### CSV Output

- `CSV_SEPARATOR`: Character to separate CSV columns (default: "|")
- `CSV_FILENAME`: Default filename for downloaded CSV

### UI Settings

- `APP_TITLE`: Application title
- `UPLOAD_LABEL`: File upload label

### Changing the Model

To use a different Ollama model:

1. Pull your preferred model: `ollama pull <model-name>`
2. Update `DEFAULT_MODEL` in `config/settings.py`

## Limitations

- Requires Ollama to be running locally
- Best results with well-structured requirement documents
- Processing time depends on document size and LLM performance

## Contributing

This is a lite version focused on core functionality. For advanced features, check out the full Spec2Test project.

## Pro Version Features

The full commercial version will include advanced features such as:

- **Advanced Prompts**: Specialized prompts per requirement type (functional, non-functional, UI, etc.)
- **Prompt Chaining**: Multi-step processing for better accuracy and context understanding
- **Semantic Search**: Intelligent search across requirements and test cases
- **Version Comparison**: Track changes between document versions and show test case evolution
- **Multi-Format Export**: Excel with formatting, Jira-ready CSV, and other enterprise formats
- **Authentication System**: Optional user management for hosted deployments
- **Custom Solutions**: Tailored versions for each client's specific requirements and workflows

## Who Can Benefit

Spec2Test Lite serves diverse users with different needs and security requirements:

### **For Privacy-Conscious Organizations**

- **Legal Firms**: Process legal requirements and contracts without exposing confidential information to third-party AI services
- **Healthcare Providers**: Handle HIPAA-compliant medical software specifications with local processing
- **Financial Institutions**: Process banking and fintech requirements while maintaining regulatory compliance
- **Government Agencies**: Handle classified or sensitive government software requirements
- **R&D Departments**: Protect proprietary business logic and trade secrets during test case generation

### **For Development Teams**

- **Software Developers**: Generate test cases from technical specifications and user stories
- **QA Engineers**: Automate test planning for complex software systems
- **Product Managers**: Transform requirement documents into actionable testing frameworks
- **DevOps Teams**: Integrate test case generation into CI/CD pipelines

### **For Training & Education**

- **Software Testing Trainers**: Generate test scenarios for training programs
- **Students**: Learn test case design from real requirements
- **Bootcamps**: Provide hands-on experience with AI-powered testing tools

### **For Compliance & Audit**

- **Compliance Officers**: Create audit trails and compliance verification test cases
- **Auditors**: Generate systematic test cases for regulatory reviews
- **Risk Managers**: Ensure comprehensive coverage of requirement testing

## License

MIT License
