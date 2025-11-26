import pandas as pd
import numpy as np

def compare_csvs_for_duplicates(file1_path, file2_path, comparison_columns=None, output_file=None):
    """
    Compare two CSV files and find duplicates between them.
    
    Args:
        file1_path (str): Path to first CSV file
        file2_path (str): Path to second CSV file  
        comparison_columns (list): Specific columns to compare (if None, will try to auto-detect)
        output_file (str): Optional output file to save results
    
    Returns:
        dict: Dictionary containing duplicate analysis results
    """
    
    print("🔍 Loading CSV files...")
    
    # Load the CSV files
    try:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        print(f"✅ File 1 loaded: {len(df1)} rows")
        print(f"✅ File 2 loaded: {len(df2)} rows")
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return None
    
    # Display column info
    print(f"\n📊 File 1 columns: {list(df1.columns)}")
    print(f"📊 File 2 columns: {list(df2.columns)}")
    
    # Auto-detect comparison columns if not specified
    if comparison_columns is None:
        common_columns = list(set(df1.columns) & set(df2.columns))
        print(f"\n🔗 Common columns found: {common_columns}")
        
        # Prioritize likely identity columns
        priority_columns = ['email', 'Email', 'Email Address', 'Primary Email', 'email address',
                          'first name', 'First Name', 'last name', 'Last Name', 'name', 'Name',
                          'id', 'ID', 'ILC ID', 'phone', 'Phone', 'Mobile Phone']
        
        comparison_columns = []
        for col in priority_columns:
            if col in common_columns:
                comparison_columns.append(col)
        
        # If no priority columns found, use all common columns
        if not comparison_columns:
            comparison_columns = common_columns[:3]  # Use first 3 common columns
        
        print(f"🎯 Using columns for comparison: {comparison_columns}")
    
    if not comparison_columns:
        print("❌ No common columns found for comparison!")
        return None
    
    # Prepare data for comparison
    print("\n🧹 Cleaning data for comparison...")
    
    def clean_data(df, columns):
        """Clean and normalize data for comparison"""
        df_clean = df.copy()
        for col in columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
        return df_clean
    
    df1_clean = clean_data(df1, comparison_columns)
    df2_clean = clean_data(df2, comparison_columns)
    
    # Find duplicates
    print("🔍 Finding duplicates...")
    results = {}
    
    # Method 1: Exact matches on all comparison columns
    if len(comparison_columns) > 1:
        df1_combined = df1_clean[comparison_columns].apply(lambda x: '|'.join(x.astype(str)), axis=1)
        df2_combined = df2_clean[comparison_columns].apply(lambda x: '|'.join(x.astype(str)), axis=1)
        
        exact_matches = df1_combined[df1_combined.isin(df2_combined)]
        exact_match_indices = exact_matches.index.tolist()
        
        results['exact_matches'] = {
            'count': len(exact_match_indices),
            'file1_rows': df1.iloc[exact_match_indices][comparison_columns + ['First Name', 'Last Name'] if 'First Name' in df1.columns else comparison_columns].to_dict('records'),
            'description': f"Exact matches on all columns: {comparison_columns}"
        }
    
    # Method 2: Column-by-column duplicates
    column_duplicates = {}
    for col in comparison_columns:
        if col in df1_clean.columns and col in df2_clean.columns:
            # Remove empty/nan values for comparison
            df1_col_clean = df1_clean[col].replace(['', 'nan', 'none'], np.nan).dropna()
            df2_col_clean = df2_clean[col].replace(['', 'nan', 'none'], np.nan).dropna()
            
            duplicates = df1_col_clean[df1_col_clean.isin(df2_col_clean)]
            duplicate_indices = duplicates.index.tolist()
            
            if len(duplicate_indices) > 0:
                display_cols = [col]
                if 'First Name' in df1.columns and 'Last Name' in df1.columns:
                    display_cols.extend(['First Name', 'Last Name'])
                
                column_duplicates[col] = {
                    'count': len(duplicate_indices),
                    'duplicates': df1.iloc[duplicate_indices][display_cols].to_dict('records'),
                    'sample_values': duplicates.head(5).tolist()
                }
    
    results['column_duplicates'] = column_duplicates
    
    # Method 3: Fuzzy name matching (if name columns exist)
    name_cols = ['First Name', 'Last Name', 'Name', 'name']
    available_name_cols = [col for col in name_cols if col in df1.columns and col in df2.columns]
    
    if available_name_cols:
        print("🔤 Checking for potential name matches...")
        # Simple fuzzy matching - you could enhance this with fuzzywuzzy library
        name_matches = []
        for idx1, row1 in df1.iterrows():
            for idx2, row2 in df2.iterrows():
                similarity_score = 0
                for col in available_name_cols:
                    if pd.notna(row1[col]) and pd.notna(row2[col]):
                        val1 = str(row1[col]).lower().strip()
                        val2 = str(row2[col]).lower().strip()
                        if val1 == val2 and val1 != '':
                            similarity_score += 1
                
                if similarity_score >= len(available_name_cols):  # All name columns match
                    name_matches.append({
                        'file1_index': idx1,
                        'file2_index': idx2,
                        'file1_data': {col: row1[col] for col in available_name_cols},
                        'file2_data': {col: row2[col] for col in available_name_cols}
                    })
        
        results['name_matches'] = {
            'count': len(name_matches),
            'matches': name_matches[:10],  # Limit to first 10 for display
            'description': f"Exact name matches on columns: {available_name_cols}"
        }
    
    # Print results
    print("\n" + "="*60)
    print("📋 DUPLICATE ANALYSIS RESULTS")
    print("="*60)
    
    if 'exact_matches' in results and results['exact_matches']['count'] > 0:
        print(f"\n🎯 EXACT MATCHES: {results['exact_matches']['count']} found")
        print(f"   Criteria: {results['exact_matches']['description']}")
        for i, match in enumerate(results['exact_matches']['file1_rows'][:5]):
            print(f"   {i+1}. {match}")
    
    if results['column_duplicates']:
        print(f"\n📊 COLUMN-BY-COLUMN DUPLICATES:")
        for col, data in results['column_duplicates'].items():
            print(f"   {col}: {data['count']} duplicates")
            print(f"      Sample values: {data['sample_values'][:3]}")
    
    if 'name_matches' in results and results['name_matches']['count'] > 0:
        print(f"\n👥 NAME MATCHES: {results['name_matches']['count']} found")
        for i, match in enumerate(results['name_matches']['matches'][:3]):
            print(f"   {i+1}. File1: {match['file1_data']} | File2: {match['file2_data']}")
    
    # Save to file if requested
    if output_file:
        print(f"\n💾 Saving detailed results to {output_file}")
        with open(output_file, 'w') as f:
            f.write("DUPLICATE ANALYSIS RESULTS\n")
            f.write("="*60 + "\n\n")
            
            for key, value in results.items():
                f.write(f"{key.upper()}:\n")
                f.write(f"Count: {value.get('count', 'N/A')}\n")
                if 'description' in value:
                    f.write(f"Description: {value['description']}\n")
                f.write("\n")
    
    return results

# Example usage and main execution
if __name__ == "__main__":
    print("🔍 CSV Duplicate Checker")
    print("="*40)
    
    # You can modify these file paths as needed
    file1 = "Master Alumni Sheet - Sheet1.csv"
    file2 = "export.csv"
    
    # Check if files exist
    import os
    if not os.path.exists(file1):
        print(f"❌ File not found: {file1}")
        print("Available files in directory:")
        for f in os.listdir("."):
            if f.endswith('.csv'):
                print(f"   📄 {f}")
        
        # Let user choose files
        print("\n📝 Enter file paths manually:")
        file1 = input("Enter path to first CSV file: ").strip()
        file2 = input("Enter path to second CSV file: ").strip()
    
    if os.path.exists(file1) and os.path.exists(file2):
        # Run the comparison
        results = compare_csvs_for_duplicates(
            file1, 
            file2, 
            comparison_columns=None,  # Auto-detect
            output_file="duplicate_analysis.txt"
        )
        
        if results:
            print("\n✅ Analysis complete! Check 'duplicate_analysis.txt' for detailed results.")
        else:
            print("\n❌ Analysis failed!")
    else:
        print("❌ One or both files not found!")
