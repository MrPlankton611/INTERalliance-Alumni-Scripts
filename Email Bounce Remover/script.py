import pandas as pd

# Load files
bounced = pd.read_csv('export.csv')
alumni = pd.read_csv('alumni.csv')

# Make sure both columns are consistent (strip spaces, lowercase)
bounced_emails = bounced['Primary Email'].str.strip().str.lower().unique()

# Use the correct column name from your alumni.csv file
alumni['Email'] = alumni['Email Address'].fillna('').astype(str).str.strip().str.lower()

# Create a copy of all alumni (keep everyone)
cleaned = alumni.copy()

# Clear email addresses for those that bounced (set to empty string)
bounced_mask = cleaned['Email'].isin(bounced_emails)
cleaned.loc[bounced_mask, 'Email Address'] = ''

# Drop the temporary Email column
cleaned = cleaned.drop(columns=['Email'])

# Save cleaned data
cleaned.to_csv('alumni_cleaned.csv', index=False)

print(f"Cleared {bounced_mask.sum()} bounced email addresses.")
print(f"Total alumni kept: {len(cleaned)}")
