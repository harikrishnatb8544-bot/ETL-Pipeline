"""
ETL Pipeline Project - CODTECH Internship Task-1
================================================

This script demonstrates a complete Data Pipeline for preprocessing, 
transformation, and loading using Pandas and Scikit-Learn.

Author: CODTECH Internship
Date: 2026
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import os
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class ETLPipeline:
    """
    A comprehensive ETL Pipeline class that handles:
    - Data extraction (loading from CSV)
    - Data preprocessing (cleaning, handling missing values)
    - Data transformation (scaling, encoding, feature engineering)
    - Data loading (saving processed data)
    """
    
    def __init__(self, input_path, output_path):
        """
        Initialize the ETL Pipeline
        
        Parameters:
        -----------
        input_path : str
            Path to the input data file
        output_path : str
            Path to save the output (processed) data
        """
        self.input_path = input_path
        self.output_path = output_path
        self.raw_data = None
        self.processed_data = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
        print("="*60)
        print("ETL PIPELINE INITIALIZED")
        print("="*60)
    
    
    def extract_data(self):
        """
        EXTRACT PHASE: Load data from the input source
        
        Returns:
        --------
        pd.DataFrame : Raw data loaded from the input file
        """
        try:
            print("\n[1] EXTRACTION PHASE")
            print("-" * 40)
            
            if not os.path.exists(self.input_path):
                raise FileNotFoundError(f"Input file not found: {self.input_path}")
            
            self.raw_data = pd.read_csv(self.input_path)
            
            print(f"✓ Data loaded successfully!")
            print(f"  - Shape: {self.raw_data.shape}")
            print(f"  - Columns: {list(self.raw_data.columns)}")
            print(f"  - Data Types:\n{self.raw_data.dtypes}")
            
            return self.raw_data
            
        except Exception as e:
            print(f"✗ Error during extraction: {str(e)}")
            raise
    
    
    def preprocess_data(self):
        """
        PREPROCESSING PHASE: Clean and prepare data
        
        Operations:
        - Handle missing values
        - Remove duplicates
        - Identify data types
        - Display data quality metrics
        """
        try:
            print("\n[2] PREPROCESSING PHASE")
            print("-" * 40)
            
            if self.raw_data is None:
                raise ValueError("No data to preprocess. Run extract_data() first.")
            
            # Create a copy to avoid modifying original data
            df = self.raw_data.copy()
            
            # Display missing values info
            print("Missing Values Analysis:")
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                print(f"  - Columns with missing values:")
                print(missing_data[missing_data > 0])
            else:
                print("  - No missing values found!")
            
            # Handle missing values
            # For numerical columns: use mean imputation
            # For categorical columns: use 'Unknown' or mode
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            
            if len(numeric_cols) > 0:
                imputer = SimpleImputer(strategy='mean')
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                print(f"  - Applied mean imputation to {len(numeric_cols)} numeric columns")
            
            if len(categorical_cols) > 0:
                imputer = SimpleImputer(strategy='most_frequent')
                df[categorical_cols] = imputer.fit_transform(df[categorical_cols])
                print(f"  - Applied mode imputation to {len(categorical_cols)} categorical columns")
            
            # Remove duplicates
            initial_rows = len(df)
            df = df.drop_duplicates()
            duplicates_removed = initial_rows - len(df)
            
            if duplicates_removed > 0:
                print(f"  - Removed {duplicates_removed} duplicate rows")
            else:
                print("  - No duplicates found!")
            
            # Data quality summary
            print(f"\nData Quality Summary:")
            print(f"  - Total rows: {len(df)}")
            print(f"  - Total columns: {len(df.columns)}")
            print(f"  - Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            self.processed_data = df
            return df
            
        except Exception as e:
            print(f"✗ Error during preprocessing: {str(e)}")
            raise
    
    
    def transform_data(self):
        """
        TRANSFORMATION PHASE: Feature engineering and scaling
        
        Operations:
        - Encode categorical variables
        - Scale numerical features
        - Create new features if applicable
        - Normalize data for better model performance
        """
        try:
            print("\n[3] TRANSFORMATION PHASE")
            print("-" * 40)
            
            if self.processed_data is None:
                raise ValueError("No data to transform. Run preprocess_data() first.")
            
            df = self.processed_data.copy()
            
            # Identify column types
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            print(f"Identified {len(numeric_cols)} numeric and {len(categorical_cols)} categorical columns")
            
            # Encode categorical variables
            if len(categorical_cols) > 0:
                print(f"\nEncoding categorical columns:")
                for col in categorical_cols:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                    print(f"  - Encoded '{col}' with {len(le.classes_)} unique values")
            
            # Scale numerical features
            if len(numeric_cols) > 0:
                print(f"\nScaling numerical features:")
                df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
                print(f"  - Standardized {len(numeric_cols)} numerical columns using StandardScaler")
                print(f"  - Mean: ~0, Std Dev: ~1")
            
            # Feature engineering example: create derived features if applicable
            if len(numeric_cols) >= 2:
                print(f"\nFeature Engineering:")
                # Example: create a ratio feature from first two numeric columns
                col1, col2 = numeric_cols[0], numeric_cols[1]
                df[f'{col1}_to_{col2}_ratio'] = df[col1] / (df[col2] + 1e-8)  # Avoid division by zero
                print(f"  - Created derived feature: '{col1}_to_{col2}_ratio'")
            
            self.processed_data = df
            print(f"\nTransformed data shape: {df.shape}")
            return df
            
        except Exception as e:
            print(f"✗ Error during transformation: {str(e)}")
            raise
    
    
    def load_data(self, filename='processed_data.csv'):
        """
        LOAD PHASE: Save the processed data to output location
        
        Parameters:
        -----------
        filename : str
            Output filename (default: 'processed_data.csv')
            
        Returns:
        --------
        str : Path to the saved file
        """
        try:
            print("\n[4] LOADING PHASE")
            print("-" * 40)
            
            if self.processed_data is None:
                raise ValueError("No data to load. Run transform_data() first.")
            
            # Create output directory if it doesn't exist
            os.makedirs(self.output_path, exist_ok=True)
            
            output_file = os.path.join(self.output_path, filename)
            
            # Save the processed data
            self.processed_data.to_csv(output_file, index=False)
            
            file_size = os.path.getsize(output_file) / 1024  # Size in KB
            
            print(f"✓ Data loaded (saved) successfully!")
            print(f"  - Output file: {output_file}")
            print(f"  - File size: {file_size:.2f} KB")
            print(f"  - Records: {len(self.processed_data)}")
            print(f"  - Columns: {len(self.processed_data.columns)}")
            
            return output_file
            
        except Exception as e:
            print(f"✗ Error during loading: {str(e)}")
            raise
    
    
    def run_pipeline(self, filename='processed_data.csv'):
        """
        Execute the complete ETL pipeline
        
        Parameters:
        -----------
        filename : str
            Output filename
            
        Returns:
        --------
        dict : Dictionary containing pipeline execution status and output path
        """
        try:
            print("\n" + "="*60)
            print("STARTING ETL PIPELINE EXECUTION")
            print("="*60)
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Execute pipeline stages
            self.extract_data()
            self.preprocess_data()
            self.transform_data()
            output_file = self.load_data(filename)
            
            # Summary
            print("\n" + "="*60)
            print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            summary = {
                'status': 'Success',
                'input_file': self.input_path,
                'output_file': output_file,
                'raw_shape': self.raw_data.shape,
                'processed_shape': self.processed_data.shape,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"\nSummary:")
            for key, value in summary.items():
                print(f"  - {key}: {value}")
            
            return summary
            
        except Exception as e:
            print("\n" + "="*60)
            print("PIPELINE EXECUTION FAILED!")
            print("="*60)
            print(f"Error: {str(e)}")
            return {'status': 'Failed', 'error': str(e)}


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    # Define paths
    input_file = "data/sample_data.csv"
    output_directory = "output"
    
    # Create ETL Pipeline instance
    pipeline = ETLPipeline(input_file, output_directory)
    
    # Run the complete ETL pipeline
    result = pipeline.run_pipeline(filename='processed_data.csv')
    
    # Display final result
    print("\n" + "="*60)
    print("FINAL RESULT:")
    print("="*60)
    if result['status'] == 'Success':
        print("✓ Pipeline completed successfully!")
        print(f"  Output saved to: {result['output_file']}")
    else:
        print(f"✗ Pipeline failed: {result['error']}")
