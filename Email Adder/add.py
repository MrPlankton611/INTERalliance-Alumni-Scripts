import pandas as pd
import os

# Change to the script's directory to find the CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load files Make sure file names match your actual files
base_alumni = pd.read_csv('alumni.csv')
email_source = pd.read_csv('add.csv')

# Clean and normalize names for matching
base_alumni['first_norm'] = base_alumni['First Name'].fillna('').astype(str).str.strip().str.lower()
base_alumni['last_norm'] = base_alumni['Last Name'].fillna('').astype(str).str.strip().str.lower()

email_source['first_norm'] = email_source['firstName'].fillna('').astype(str).str.strip().str.lower()
email_source['last_norm'] = email_source['lastName'].fillna('').astype(str).str.strip().str.lower()

# Create a copy of base alumni (keep everyone)
enhanced = base_alumni.copy()

# Add Email Address column if it doesn't exist
if 'Email Address' not in enhanced.columns:
    enhanced['Email Address'] = ''

# Create email mapping from source file
email_mapping = {}
email_count = 0
for _, row in email_source.iterrows():
    key = (row['first_norm'], row['last_norm'])
    # Use proEmail since linkedinEmail is mostly empty
    email = row.get('proEmail', '')
    if pd.notna(email) and str(email).strip() != '':
        email_mapping[key] = str(email).strip()
        email_count += 1
print(email_count, "emails loaded from source file.")
# Match names and add emails
emails_added = 0
for idx, row in enhanced.iterrows():
    key = (row['first_norm'], row['last_norm'])
    
    if key in email_mapping:
        current_email = enhanced.iloc[idx]['Email Address']
        # Only add if email slot is empty
        if pd.isna(current_email) or str(current_email).strip() == '':
            enhanced.iloc[idx, enhanced.columns.get_loc('Email Address')] = email_mapping[key]
            emails_added += 1

# Drop temporary columns
enhanced = enhanced.drop(columns=['first_norm', 'last_norm'])

# Save enhanced data
enhanced.to_csv('alumni_with_emails.csv', index=False)

print(f"Added {emails_added} email addresses.")
print(f"Total alumni kept: {len(enhanced)}")