import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from core.generator import parse_llm_csv_output


def run_samples():
    samples = [
        "Title|Description\nLogin works|User can login\nLogout works|User can logout",
        "ID|Title|Description\n1|Login works|User can login\n2|Logout works|User can logout",
        "Some preface text...\nTitle|Description\nA|B\nC|D\nSome epilogue text",
        "No CSV here",
        "",
    ]
    for i, s in enumerate(samples, 1):
        df = parse_llm_csv_output(s)
        print(f"Sample {i}: shape={df.shape}, cols={list(df.columns)}")
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("<empty>")
        print("-" * 40)


if __name__ == "__main__":
    run_samples() 