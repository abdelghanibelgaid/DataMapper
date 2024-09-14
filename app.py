# app.py

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    st.title("Database Column Mapper")

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

        # Perform column mapping
        column_mapping, similarity_matrix = map_columns(df1, df2)

        st.subheader("Column Mapping Based on Description Similarity")
        mapping_df = pd.DataFrame(list(column_mapping.items()), columns=['Column from File 1', 'Mapped to Column in File 2'])
        st.dataframe(mapping_df)

        # Display similarity matrix as heatmap
        st.subheader("Similarity Matrix Heatmap")
        display_heatmap(similarity_matrix, df1['Column Name'], df2['Column Name'])

        # Generate mapping function
        st.subheader("Generated Mapping Function")
        st.code(generate_mapping_function(column_mapping), language='python')

def map_columns(df1, df2):
    # Get descriptions
    descriptions_1 = df1['Description'].fillna('').tolist()
    descriptions_2 = df2['Description'].fillna('').tolist()

    # Vectorize descriptions using TF-IDF
    vectorizer = TfidfVectorizer().fit(descriptions_1 + descriptions_2)
    tfidf_matrix_1 = vectorizer.transform(descriptions_1)
    tfidf_matrix_2 = vectorizer.transform(descriptions_2)

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix_1, tfidf_matrix_2)

    # Create mapping based on highest similarity
    column_mapping = {}
    for i, row in enumerate(similarity_matrix):
        best_match_index = row.argmax()
        col_1 = df1['Column Name'].iloc[i]
        col_2 = df2['Column Name'].iloc[best_match_index]
        column_mapping[col_1] = col_2

    return column_mapping, similarity_matrix

def generate_mapping_function(column_mapping):
    mapping_lines = ["def map_columns(df_source, df_target):", "    # Column mapping"]
    mapping_lines.append(f"    column_mapping = {column_mapping}")
    mapping_lines.append("    for src_col, tgt_col in column_mapping.items():")
    mapping_lines.append("        if src_col in df_source.columns and tgt_col in df_target.columns:")
    mapping_lines.append("            df_target[tgt_col] = df_source[src_col]")
    mapping_lines.append("    return df_target")
    return '\n'.join(mapping_lines)

def display_heatmap(similarity_matrix, columns_1, columns_2):
    import seaborn as sns
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=True, fmt=".2f", cmap="YlGnBu",
                xticklabels=columns_2, yticklabels=columns_1, ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    st.pyplot(fig)

if __name__ == '__main__':
    main()
