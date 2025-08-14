import pandas as pd
import subprocess
import io
import re


from config.settings import DEFAULT_MODEL, TIMEOUT_SECONDS

def run_llm(prompt, model=DEFAULT_MODEL):
    cmd = [
        "ollama", "run", model, prompt
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=TIMEOUT_SECONDS)
        if result.returncode != 0:
            raise Exception(f"Ollama command failed: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise Exception("LLM request timed out. Try with a smaller document or different model.")
    except FileNotFoundError:
        raise Exception("Ollama not found. Please install Ollama and ensure it's in your PATH.")
    except Exception as e:
        raise Exception(f"Error running LLM: {str(e)}")


from config.settings import CSV_SEPARATOR

def parse_llm_csv_output(output_text):
    output_text = output_text.strip()

    # Extract the CSV block starting with "Title|Description" header, up to the last line
    csv_match = re.search(r"(Title\s*\|\s*Description\s*\n(?:.*\|.*\n?)*)", output_text, re.IGNORECASE)
    if not csv_match:
        return pd.DataFrame(columns=["Title", "Description"])

    csv_text = csv_match.group(1).strip()

    # Remove any trailing notes or lines that do not look like CSV rows
    # Keep only lines that have exactly one separator
    lines = csv_text.splitlines()
    filtered_lines = [lines[0]]  # header
    
    for line in lines[1:]:
        if re.search(r'ID:\s*Title:\s*Title\s*Description:\s*Description', line, re.IGNORECASE):
            continue
            
        # Count separators; accept line only if exactly one separator (meaning 2 columns)
        if line.count(CSV_SEPARATOR) == 1:
            filtered_lines.append(line)
        else:
            # Stop parsing once non-CSV row encountered (e.g., notes)
            break

    csv_text_clean = "\n".join(filtered_lines)

    try:
        df = pd.read_csv(io.StringIO(csv_text_clean), sep=CSV_SEPARATOR)
        if {"Title", "Description"}.issubset(df.columns):
            df = df[["Title", "Description"]]

            # Drop placeholders and empty rows
            df = df[~((df["Title"].str.strip().isin(["-", "N/A", ""])) |
                      (df["Description"].str.strip().isin(["-", "N/A", ""])))]
            df = df.reset_index(drop=True)

            if df.empty:
                return pd.DataFrame(columns=["Title", "Description"])

            return df
        else:
            return pd.DataFrame(columns=["Title", "Description"])
    except Exception:
        return pd.DataFrame(columns=["Title", "Description"])


        