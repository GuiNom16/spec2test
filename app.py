import streamlit as st
from core.parser import parse_file, clean_text, clean_test_cases_df, add_test_case_ids
from core.chunker import chunk_text
from core.prompt import get_prompt
from core.generator import run_llm, parse_llm_csv_output
import pandas as pd
import io

st.title("Spec2Test Lite - AI Test Case Generator")

uploaded_file = st.file_uploader("Upload DOCX or PDF", type=["docx", "pdf"])

if uploaded_file:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Parse and clean text to remove intro/TOC
    text = parse_file(file_path)
    cleaned_text = clean_text(text)

    # Chunk cleaned text for LLM input
    chunks = chunk_text(cleaned_text)

    all_dfs = []
    for i, chunk in enumerate(chunks):
        st.write(f"Processing chunk {i+1}/{len(chunks)}...")
        prompt = get_prompt(chunk)
        output = run_llm(prompt)
        #testing 
        st.text_area(f"Raw LLM output for chunk {i+1}", output, height=200)


        df = parse_llm_csv_output(output)
        all_dfs.append(df)

    # Keep only non-empty DataFrames
    non_empty_dfs = [df for df in all_dfs if df is not None and not df.empty]

    if non_empty_dfs:
        # Combine all DataFrames from chunks
        result_df = pd.concat(non_empty_dfs, ignore_index=True)

        # Clean test cases: keep rows with non-empty Title
        result_df = clean_test_cases_df(result_df)

        if not result_df.empty:
            # Add sequential IDs locally since AI no longer provides them
            result_df = add_test_case_ids(result_df)

            # Display the results
            st.dataframe(result_df)

            # Prepare CSV for download
            csv_buffer = io.StringIO()
            result_df.to_csv(csv_buffer, index=False, sep="|")
            csv_data = csv_buffer.getvalue()

            st.download_button("Download CSV", csv_data, "spec2test_output.csv", "text/csv")
        else:
            st.warning("No valid test cases could be extracted from the model output.")
    else:
        st.warning("No test cases were generated. Try a different document or adjust the prompt.")
