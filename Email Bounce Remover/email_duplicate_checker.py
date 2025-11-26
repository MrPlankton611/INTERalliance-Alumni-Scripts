# Simple Email Duplicate Checker
import pandas as pd

def find_email_duplicates(alumni_file, bounced_file):
    """Find email duplicates between alumni and bounced email lists"""
    
    print("📧 Email Duplicate Analysis")
    print("="*40)
    
    # Load files
    alumni = pd.read_csv(alumni_file)
    bounced = pd.read_csv(bounced_file)
    
    print(f"Alumni records: {len(alumni)}")
    print(f"Bounced emails: {len(bounced)}")
    
    # Clean email data
    alumni_emails = alumni['Email Address'].fillna('').astype(str).str.strip().str.lower()
    bounced_emails = bounced['Primary Email'].fillna('').astype(str).str.strip().str.lower()
    
    # Remove empty emails
    alumni_emails_clean = alumni_emails[alumni_emails != ''].drop_duplicates()
    bounced_emails_clean = bounced_emails[bounced_emails != ''].drop_duplicates()
    
    print(f"\nClean alumni emails: {len(alumni_emails_clean)}")
    print(f"Clean bounced emails: {len(bounced_emails_clean)}")
    
    # Find duplicates
    email_matches = alumni_emails_clean[alumni_emails_clean.isin(bounced_emails_clean)]
    
    print(f"\n🔍 Email matches found: {len(email_matches)}")
    
    if len(email_matches) > 0:
        print("\nSample matches:")
        for i, email in enumerate(email_matches.head(10)):
            # Find the alumni with this email
            alumni_with_email = alumni[alumni['Email Address'].str.lower().str.strip() == email]
            if len(alumni_with_email) > 0:
                first_match = alumni_with_email.iloc[0]
                print(f"  {i+1}. {email} -> {first_match.get('First Name', 'N/A')} {first_match.get('Last Name', 'N/A')}")
    
    return email_matches

# Run the email duplicate check
if __name__ == "__main__":
    matches = find_email_duplicates('alumni_cleaned.csv', 'export.csv')
