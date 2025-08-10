import fitz  # PyMuPDF
import docx


def parse_file(file_path):
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file type")


def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    return text


def parse_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def clean_text(text):
    # Naive approach: find first occurrence of "Requirement" or "REQ"
    keywords = ["Requirement", "REQ", "Functional Requirement"]
    indices = [text.find(k) for k in keywords if text.find(k) != -1]
    if indices:
        start = min(indices)
        return text[start:]
    return text  # fallback to full text if no keyword found


def clean_test_cases_df(df):
    # Keep rows with non-empty Title
    cleaned_df = df[df["Title"].str.strip().astype(bool)].copy()
    return cleaned_df.reset_index(drop=True)



def add_test_case_ids(df):
    df = df.copy()
    df["ID"] = [f"TC-{i+1:03d}" for i in range(len(df))]
    # Optional: reorder columns so ID is first
    cols = ["ID"] + [c for c in df.columns if c != "ID"]
    return df[cols]
