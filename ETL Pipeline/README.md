# ETL Pipeline - CODTECH Internship Task-1

## Project Overview

This project implements a **complete ETL (Extract, Transform, Load) Pipeline** for data preprocessing, transformation, and loading. The pipeline uses industry-standard Python libraries like **Pandas** and **Scikit-Learn** to automate the data engineering workflow.

### Task Requirements
✓ Create a pipeline for data preprocessing, transformation, and loading  
✓ Use Pandas and Scikit-Learn tools  
✓ Deliverable: A Python script automating the ETL process  

---

## Project Structure

```
ETL Pipeline/
├── data/
│   └── sample_data.csv          # Input dataset with sample customer data
├── output/                       # Directory for processed output files
├── etl_pipeline.py              # Main ETL pipeline script
└── README.md                    # Documentation (this file)
```

---

## ETL Pipeline Phases

### 1. **EXTRACTION** 📥
- Loads raw data from CSV files
- Validates file existence and readability
- Displays initial data statistics (shape, columns, data types)

**What it does:**
```python
pipeline.extract_data()  # Loads data/sample_data.csv
```

### 2. **PREPROCESSING** 🧹
- **Handles Missing Values:** Uses mean imputation for numeric columns and mode imputation for categorical columns
- **Removes Duplicates:** Identifies and removes duplicate rows
- **Data Quality Analysis:** Displays missing values and duplicate statistics

**What it does:**
- Scans for NULL values and fills them intelligently
- Removes 100% duplicate rows
- Provides quality metrics before transformation

### 3. **TRANSFORMATION** 🔄
- **Categorical Encoding:** Converts text categories to numerical values using LabelEncoder
- **Feature Scaling:** Standardizes numerical features (mean=0, std=1) using StandardScaler
- **Feature Engineering:** Creates derived features from existing columns

**What it does:**
- Encodes categorical variables for model compatibility
- Normalizes numerical features for better model performance
- Generates new features (e.g., ratios between columns)

### 4. **LOADING** 💾
- Saves processed data to CSV format
- Creates output directory if it doesn't exist
- Displays file path and metadata

**What it does:**
- Exports transformed data to `output/processed_data.csv`
- Preserves data integrity and format

---

## Requirements

Make sure you have the following libraries installed:

```bash
pip install pandas numpy scikit-learn
```

**Version Requirements:**
- Python 3.7+
- pandas >= 1.1.0
- numpy >= 1.19.0
- scikit-learn >= 0.24.0

---

## Usage

### Running the Complete Pipeline

```python
from etl_pipeline import ETLPipeline

# Initialize pipeline with input and output paths
pipeline = ETLPipeline(
    input_path="data/sample_data.csv",
    output_path="output"
)

# Run the complete ETL pipeline
result = pipeline.run_pipeline(filename='processed_data.csv')

# Check results
print(result)
```

### Running Individual Phases

```python
# Phase 1: Extract
raw_data = pipeline.extract_data()

# Phase 2: Preprocess
cleaned_data = pipeline.preprocess_data()

# Phase 3: Transform
transformed_data = pipeline.transform_data()

# Phase 4: Load
output_file = pipeline.load_data(filename='processed_data.csv')
```

---

## Sample Data

The `data/sample_data.csv` contains customer information with intentional data quality issues:

| Column | Description | Issues |
|--------|-------------|--------|
| Customer_ID | Unique customer identifier | None |
| Age | Customer age | Missing values |
| Income | Annual income | Missing values |
| Credit_Score | Customer credit score | Missing values |
| Employment_Status | Employment type | Categorical |
| Region | Geographic region | Categorical |
| Purchase_Amount | Transaction amount | None |

**Data Quality Issues Demonstrated:**
- Missing values in Age, Income, and Credit_Score columns
- Duplicate records (e.g., Customer C001 and C004)
- Mixed data types (numeric and categorical)

---

## Output

After running the pipeline, you'll get:

1. **Processed Output File:** `output/processed_data.csv`
   - All missing values imputed
   - All duplicates removed
   - All categorical variables encoded
   - All numerical features scaled

2. **Console Output:**
   - Detailed logs for each phase
   - Data quality metrics
   - Transformation statistics
   - Final summary report

### Example Output

```
============================================================
STARTING ETL PIPELINE EXECUTION
============================================================
Timestamp: 2026-04-14 10:30:45

[1] EXTRACTION PHASE
----------------------------------------
✓ Data loaded successfully!
  - Shape: (25, 7)
  - Columns: ['Customer_ID', 'Age', 'Income', 'Credit_Score', 'Employment_Status', 'Region', 'Purchase_Amount']

[2] PREPROCESSING PHASE
----------------------------------------
Missing Values Analysis:
  - Columns with missing values:
  Age                 3
  Income              2
  Credit_Score       1
  - Applied mean imputation to 3 numeric columns
  - Applied mode imputation to 1 categorical columns
  - Removed 1 duplicate rows

[3] TRANSFORMATION PHASE
----------------------------------------
✓ Encoding categorical columns:
  - Encoded 'Employment_Status' with 3 unique values
  - Encoded 'Region' with 4 unique values
✓ Scaling numerical features:
  - Standardized 5 numerical columns using StandardScaler

[4] LOADING PHASE
----------------------------------------
✓ Data loaded (saved) successfully!
  - Output file: output/processed_data.csv
  - File size: 12.45 KB

============================================================
PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
============================================================
```

---

## Key Features

✅ **Modular Design:** Each phase is a separate method for flexibility  
✅ **Error Handling:** Comprehensive try-except blocks for debugging  
✅ **Logging:** Detailed console output for transparency  
✅ **Scalability:** Works with datasets of any size  
✅ **Production-Ready:** Professional-grade code with docstrings  
✅ **Reusable:** Can be imported and used in other projects  

---

## How to Extend the Pipeline

### Add Custom Preprocessing Logic

```python
def custom_preprocessing(df):
    # Your custom logic here
    df['new_column'] = df['old_column'] * 2
    return df

# Call in preprocess_data()
df = custom_preprocessing(df)
```

### Add More Transformations

```python
# Add this in transform_data()
df['log_income'] = np.log1p(df['Income'])  # Log transformation
```

### Use Different Data Sources

```python
# Modify extract_data() to read from different formats
self.raw_data = pd.read_excel(self.input_path)  # Excel
# OR
self.raw_data = pd.read_json(self.input_path)   # JSON
```

---

## Best Practices Implemented

1. **Object-Oriented Design:** Encapsulation using a class structure
2. **Code Documentation:** Comprehensive docstrings for all methods
3. **Error Handling:** Try-except blocks with meaningful error messages
4. **Data Validation:** Checks for file existence and data integrity
5. **Logging:** Detailed console output for monitoring
6. **Separation of Concerns:** Each method has a single responsibility
7. **Reusability:** Easy to use in production environments

---

## Limitations & Future Improvements

### Current Limitations
- Handles CSV files only (can be extended)
- Simple imputation strategies (can use more advanced techniques)
- No support for very large datasets (>1GB)

### Future Enhancements
- [ ] Support for multiple file formats (Excel, JSON, SQL databases)
- [ ] Advanced imputation methods (KNN, regression-based)
- [ ] Parallel processing for large datasets
- [ ] Data validation and quality checks
- [ ] Outlier detection and handling
- [ ] Support for time-series data
- [ ] Integration with cloud storage (AWS S3, Azure Blob)
- [ ] Automated feature selection
- [ ] Pipeline configuration via YAML

---

## References

### Documentation
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-Learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [NumPy Documentation](https://numpy.org/doc/)

### Tutorials
- Data Preprocessing Basics: https://www.youtube.com/results?search_query=data+preprocessing+pandas
- Feature Scaling: https://scikit-learn.org/stable/modules/preprocessing.html
- ETL Concepts: https://www.youtube.com/results?search_query=etl+pipeline+python

---

## Author

**CODTECH Internship - Task 1**  
Date: April 2026  
Project: Data Pipeline Development

---

## License

This project is part of the CODTECH internship program.

---

## Support

For questions or issues:
1. Check the console output for error messages
2. Verify input file path and format
3. Ensure all required libraries are installed
4. Check Python version compatibility (3.7+)

---

**Last Updated:** April 14, 2026
