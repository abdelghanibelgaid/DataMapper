# Database Mapper

This Streamlit app allows you to upload two Excel files containing database metadata and automatically maps columns based on the similarity of their descriptions. It also generates a function to perform the data mapping between the columns.

## Features

- **Upload Excel Files**: Upload two Excel files with metadata (Table Name, Column Name, Description).
- **Automatic Column Mapping**: Maps columns based on the similarity of their descriptions using TF-IDF vectorization and cosine similarity.
- **Visualization**: Displays the column mappings and a heatmap of the similarity scores.
- **Generated Function**: Provides a Python function to map data from one DataFrame to another based on the column mappings.

## How to Run the App

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/database-column-mapper.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd database-column-mapper
   ```

3. **Install Dependencies**

   Install the required Python packages using:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**

   ```bash
   streamlit run app.py
   ```

   This will open the app in your default web browser.

## How to Use the App

1. **Prepare Your Excel Files**

   - Each Excel file should contain three columns:
     - `Table Name`
     - `Column Name`
     - `Description`
   - You can use the provided `transaction_metadata.xlsx` and `deal_metadata.xlsx` files as examples.

2. **Upload the Files**

   - In the app interface, use the file uploaders to upload your two Excel files.

3. **View Column Mappings**

   - After uploading, the app will display the column mappings based on the similarity of the descriptions.

4. **Visualize Similarity Scores**

   - A heatmap will show the similarity scores between each pair of columns.

5. **Get the Mapping Function**

   - The app will generate and display a Python function that can be used to map data from one DataFrame to another based on the column mappings.

## Sample Data

Sample Excel files are provided to test the app:

- `transaction_metadata.xlsx`
- `deal_metadata.xlsx`

You can generate these files using the `generate_excel_files.py` script provided in the repository.

## Dependencies

- **Python Packages**:
  - `streamlit`
  - `pandas`
  - `scikit-learn`
  - `matplotlib`
  - `seaborn`
  - `openpyxl`

Install them using:

```bash
pip install -r requirements.txt
```

## Project Structure

```
database-column-mapper/
│
├── app.py                   # Main Streamlit app code
├── requirements.txt         # List of required Python packages
├── transaction_metadata.xlsx  # Sample metadata Excel file for the transaction table
├── deal_metadata.xlsx         # Sample metadata Excel file for the deal table
├── generate_excel_files.py    # Script to generate sample Excel files
└── README.md                # Project documentation
```

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact me.
