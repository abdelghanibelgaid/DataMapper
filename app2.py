# app2.py

import streamlit as st
import pandas as pd
import openai  # Assumes openai package is installed

def main():
    st.title("DataMapper with LLM")

    # Input for API key
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")
        return
    
    openai.api_key = api_key  # Set the API key for OpenAI client

    st.write("""
    Upload two Excel files containing the metadata of your databases. Each file should have the following columns:
    - **Table Name**
    - **Column Name**
    - **Description**
    """)

    # Upload Excel files
    uploaded_file1 = st.file_uploader("Upload First Excel File", type=["xlsx", "xls"], key="file1")
    uploaded_file2 = st.file_uploader("Upload Second Excel File", type=["xlsx", "xls"], key="file2")

    if uploaded_file1 and uploaded_file2:
        # Read Excel files
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        # Ensure required columns are present
        required_columns = {'Table Name', 'Column Name', 'Description'}
        if not required_columns.issubset(df1.columns) or not required_columns.issubset(df2.columns):
            st.error("Both files must contain 'Table Name', 'Column Name', and 'Description' columns.")
            return

        # Perform column mapping using LLM
        column_mapping = map_columns_with_llm(df1, df2)

        st.subheader("Column Mapping Based on LLM")
        mapping_df = pd.DataFrame(list(column_mapping.items()), columns=['Column from File 1', 'Mapped to Column in File 2'])
        st.dataframe(mapping_df)

        # Generate mapping function
        st.subheader("Generated Mapping Function")
        st.code(generate_mapping_function(column_mapping), language='python')

def map_columns_with_llm(df1, df2):
    # Initialize mapping dictionary
    column_mapping = {}

    # Iterate through each description in df1 and find best match in df2 using LLM
    for index1, row1 in df1.iterrows():
        description_1 = row1['Description']
        column_1 = row1['Column Name']

        best_match_column = None
        best_match_score = 0

        for index2, row2 in df2.iterrows():
            description_2 = row2['Description']
            column_2 = row2['Column Name']

            # Use LLM to determine similarity score between descriptions
            response = openai.Completion.create(
                model="gpt-4",
                prompt=f"Match the following descriptions based on similarity:\n\n"
                       f"Description 1: {description_1}\n"
                       f"Description 2: {description_2}\n\n"
                       f"On a scale from 0 to 1, where 1 means identical and 0 means completely different, "
                       f"what is the similarity score between these two descriptions?",
                max_tokens=5,
                temperature=0
            )
            similarity_score = float(response.choices[0].text.strip())

            # Update best match if similarity score is higher
            if similarity_score > best_match_score:
                best_match_score = similarity_score
                best_match_column = column_2

        # Map columns based on best similarity score
        column_mapping[column_1] = best_match_column

    return column_mapping

def generate_mapping_function(column_mapping):
    mapping_lines = ["def map_columns(df_source, df_target):", "    # Column mapping"]
    mapping_lines.append(f"    column_mapping = {column_mapping}")
    mapping_lines.append("    for src_col, tgt_col in column_mapping.items():")
    mapping_lines.append("        if src_col in df_source.columns and tgt_col in df_target.columns:")
    mapping_lines.append("            df_target[tgt_col] = df_source[src_col]")
    mapping_lines.append("    return df_target")
    return '\n'.join(mapping_lines)

if __name__ == '__main__':
    main()
