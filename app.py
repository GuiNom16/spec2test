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

st.markdown("""
Transform your software requirements documents into comprehensive test cases using AI. 
Upload a PDF or DOCX file and get structured test cases ready for your testing team.
""")

# File upload section
st.subheader("📄 Upload Requirements Document")
uploaded_file = st.file_uploader(UPLOAD_LABEL, type=["docx", "pdf"], help="Supported formats: PDF, DOCX")

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
            st.error("❌ No content could be extracted from the document.")
            st.info("💡 Make sure your document contains readable text and is not corrupted.")
        else:
            st.subheader("🔄 Processing Document")
            st.info(f"📊 Document split into {len(chunks)} sections for analysis")
            all_dfs = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, chunk in enumerate(chunks):
                status_text.text(f"🤖 Analyzing requirements chunk {i+1}/{len(chunks)}...")
                
                prompt = get_prompt(chunk)
                output = run_llm(prompt)
                df = parse_llm_csv_output(output)
                
                if df is not None and not df.empty:
                    all_dfs.append(df)
                    status_text.text(f"✅ Found {len(df)} test cases in chunk {i+1}")
                else:
                    status_text.text(f"📝 No test cases found in chunk {i+1}")
                
                progress_bar.progress((i + 1) / len(chunks))
            
            status_text.text("🎉 Processing complete!")
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
                    st.subheader("📋 Generated Test Cases")
                    st.success(f"✅ Successfully generated {len(result_df)} test cases!")
                    
                    # Show summary stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Test Cases", len(result_df))
                    with col2:
                        st.metric("Average Title Length", f"{result_df['Title'].str.len().mean():.0f} chars")
                    with col3:
                        st.metric("Average Description Length", f"{result_df['Description'].str.len().mean():.0f} chars")
                    
                    st.dataframe(result_df, use_container_width=True)

                    # Prepare CSV for download
                    csv_buffer = io.StringIO()
                    result_df.to_csv(csv_buffer, index=False, sep=CSV_SEPARATOR)
                    csv_data = csv_buffer.getvalue()

                    st.subheader("💾 Download Results")
                    st.download_button(
                        "📥 Download Test Cases as CSV", 
                        data=csv_data, 
                        file_name=CSV_FILENAME, 
                        mime="text/csv",
                        help="Download the generated test cases in CSV format for import into test management tools"
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
