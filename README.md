# Interalliance Alumni Script

Alumni email management tools for cleaning, enhancing, and maintaining alumni databases.

## 📁 Project Structure

```
Interalliance Alumni Script/
├── Email Bounce Remover/
│   ├── script.py                 # Main bounce removal script
│   ├── csvchecker.py            # Compare CSVs for duplicates
│   └── email_duplicate_checker.py # Check email duplicates
└── Email Adder/
    └── add.py                   # Add professional emails
```

## 🚀 Quick Start

### Prerequisites
```bash
# Install required Python package
pip install pandas
```

### File Setup
Place your CSV files in the same directory as the scripts you want to run.

---

## 📧 Email Bounce Remover

### Purpose
Removes bounced/invalid email addresses from alumni database while preserving all records.

### Required Files
- `alumni.csv` - Alumni database with `Email Address` column
- `export.csv` - Bounced emails with `Primary Email` column

### How to Run
```bash
# Navigate to the Email Bounce Remover directory
cd "Email Bounce Remover"

# Run the bounce removal script
python3 script.py
```

### Output
- `alumni_cleaned.csv` - Clean database with bounced emails cleared
- Reports number of emails cleared and alumni preserved

### What it Does
✅ Keeps all alumni records  
✅ Clears only bounced email addresses  
✅ Preserves all other data  

---

## ➕ Email Adder

### Purpose
Enriches alumni database by adding professional email addresses from external sources.

### Required Files
- `alumni.csv` - Base alumni database with `First Name`, `Last Name`, `Email Address`
- `add.csv` - Email source with `firstName`, `lastName`, `proEmail`

### How to Run
```bash
# Navigate to the Email Adder directory
cd "Email Adder"

# Run the email addition script
python3 add.py
```

### Output
- `alumni_with_emails.csv` - Enhanced database with added emails
- Reports number of emails added

### What it Does
✅ Matches alumni by name  
✅ Adds professional emails to empty fields only  
✅ Never overwrites existing emails  
✅ Preserves all original data  

---

## 🔍 Duplicate Checking Tools

### CSV Checker (`csvchecker.py`)
Comprehensive duplicate analysis between two CSV files.

```bash
# Navigate to the Email Bounce Remover directory
cd "Email Bounce Remover"

# Run the CSV checker tool
python3 csvchecker.py
```

**Features:**
- Exact record matches
- Column-by-column duplicates
- Name matching
- Detailed reports

### Email Duplicate Checker (`email_duplicate_checker.py`)
Specialized tool for finding duplicate email addresses.

```bash
# Navigate to the Email Bounce Remover directory
cd "Email Bounce Remover"

# Run the email duplicate checker
python3 email_duplicate_checker.py
```

---

## 📋 Common Workflows

### 1. Clean Bounced Emails
```bash
# Navigate to Email Bounce Remover directory
cd "Email Bounce Remover"

# Run the bounce removal script
python3 script.py

# Input: alumni.csv + export.csv
# Output: alumni_cleaned.csv
```

### 2. Add Professional Emails
```bash
# Navigate to Email Adder directory
cd "Email Adder"

# Run the email addition script
python3 add.py

# Input: alumni.csv + add.csv
# Output: alumni_with_emails.csv
```

### 3. Check for Duplicates
```bash
# Navigate to Email Bounce Remover directory
cd "Email Bounce Remover"

# Run interactive duplicate analysis
python3 csvchecker.py
```

### 4. Complete Email Management Pipeline
1. Start with base alumni database
2. Add professional emails using Email Adder
3. Remove bounced emails using Email Bounce Remover
4. Verify with duplicate checkers

---

## 📊 Expected CSV Formats

### Alumni Database (`alumni.csv`)
```csv
First Name,Last Name,Email Address,High School,Grad Year
John,Smith,john@email.com,ABC High,2020
Jane,Doe,,XYZ School,2021
```

### Bounced Emails (`export.csv`)
```csv
Primary Email,Bounce Reason
john@invalid.com,Invalid domain
old@email.com,User unknown
```

### Email Source (`add.csv`)
```csv
firstName,lastName,proEmail
John,Smith,john.smith@company.com
Jane,Doe,jane.doe@business.com
```

---

## ⚠️ Important Notes

### Data Safety
- **Original files are never modified**
- **All scripts create new output files**
- **Alumni records are never deleted**
- **Always backup your data before processing**

### File Requirements
- CSV files must be in UTF-8 encoding
- Column headers must match expected names
- Files should be in the same directory as scripts

### Performance
- Tested with databases up to 6,000+ records
- Professional email matching success rate: ~20-25%
- Memory usage scales with file size

---

## 🐛 Troubleshooting

### Common Issues
```bash
# File not found
FileNotFoundError: 'alumni.csv'
→ Ensure CSV files are in the script directory

# Column not found
KeyError: 'Email Address'
→ Check CSV headers match expected format

# No matches found
0 emails added/cleared
→ Verify data format and name matching
```

### Getting Help
- Check file paths and working directory
- Verify CSV column headers
- Ensure proper CSV formatting
- Test with small sample files first

---

## 📈 Results Example

```
Email Bounce Remover:
✅ Cleared 245 bounced email addresses
✅ Total alumni kept: 5,847

Email Adder:
✅ Added 352 professional email addresses  
✅ Total alumni kept: 5,847
✅ Total with emails: 4,832
```

---

## 🔧 Technical Details

**Language:** Python 3.7+  
**Dependencies:** pandas  
**License:** MIT  
**Author:** Shamgar David