# Model Configuration
DEFAULT_MODEL = "llama3"
CHUNK_SIZE = 1000  # Maximum characters per chunk
TIMEOUT_SECONDS = 60  # LLM request timeout

# File Processing
SUPPORTED_FORMATS = [".pdf", ".docx"]
TEMP_FILE_PREFIX = "temp_"

# CSV Configuration
CSV_SEPARATOR = "|"
CSV_FILENAME = "spec2test_output.csv"

# UI Configuration
APP_TITLE = "Spec2Test Lite - AI Test Case Generator"
UPLOAD_LABEL = "Upload DOCX or PDF" 