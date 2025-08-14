import streamlit as st
from core.parser import parse_file, clean_text, clean_test_cases_df, add_test_case_ids
from core.chunker import chunk_text
from core.prompt import get_prompt
from core.generator import run_llm, parse_llm_csv_output
import pandas as pd
import io
import os
from config.settings import *

st.title(APP_TITLE)

uploaded_file = st.file_uploader(UPLOAD_LABEL, type=["docx", "pdf"])

if uploaded_file:
    file_path = f"{TEMP_FILE_PREFIX}{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        # Parse and clean text to remove intro/TOC
        text = parse_file(file_path)
        cleaned_text = clean_text(text)

        # Chunk cleaned text for LLM input
        chunks = chunk_text(cleaned_text, max_chars=CHUNK_SIZE)
        
        if not chunks:
            st.error("No content could be extracted from the document.")
        else:
            all_dfs = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, chunk in enumerate(chunks):
                status_text.text(f"Processing chunk {i+1}/{len(chunks)}...")
                prompt = get_prompt(chunk)
                output = run_llm(prompt)
                
                df = parse_llm_csv_output(output)
                if df is not None and not df.empty:
                    all_dfs.append(df)
                
                progress_bar.progress((i + 1) / len(chunks))
            
            status_text.text("Processing complete!")
            progress_bar.empty()

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
                    st.success(f"✅ Generated {len(result_df)} test cases!")
                    st.dataframe(result_df)

                    # Prepare CSV for download
                    csv_buffer = io.StringIO()
                    result_df.to_csv(csv_buffer, index=False, sep=CSV_SEPARATOR)
                    csv_data = csv_buffer.getvalue()

                    st.download_button(
                        "📥 Download CSV", 
                        data=csv_data, 
                        file_name=CSV_FILENAME, 
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No valid test cases could be extracted from the model output.")
            else:
                st.warning("⚠️ No test cases were generated. Try a different document or adjust the prompt.")
    
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        st.info("💡 Make sure Ollama is running and you have the llama3 model installed.")
    
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
