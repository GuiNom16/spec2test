import pandas as pd
import subprocess
import io
import re


def run_llm(prompt, model="llama3"):
    cmd = [
        "ollama", "run", model, prompt
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.stdout.strip()


def parse_llm_csv_output(output_text):
    output_text = output_text.strip()

    # Extract the CSV block starting with "Title|Description" header, up to the last line
    csv_match = re.search(r"(Title\s*\|\s*Description\s*\n(?:.*\|.*\n?)*)", output_text, re.IGNORECASE)
    if not csv_match:
        return pd.DataFrame(columns=["Title", "Description"])

    csv_text = csv_match.group(1).strip()

    # Remove any trailing notes or lines that do not look like CSV rows
    # Keep only lines that have exactly one '|' separator
    lines = csv_text.splitlines()
    filtered_lines = [lines[0]]  # header
    for line in lines[1:]:
        # Count pipes; accept line only if exactly one pipe (meaning 2 columns)
        if line.count("|") == 1:
            filtered_lines.append(line)
        else:
            # Stop parsing once non-CSV row encountered (e.g., notes)
            break

    csv_text_clean = "\n".join(filtered_lines)

    try:
        df = pd.read_csv(io.StringIO(csv_text_clean), sep="|")
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


        