import pandas as pd
import uuid

def validate_uuid(uuid_string):
    try:
        uuid.UUID(uuid_string)
    except ValueError:
        return False
    return True

def validate_csv(file_path):
    df = pd.read_csv(file_path, sep=',', skipinitialspace=True)
    columns = ['ID', 'Platform', 'Category', 'Cookie / Data Key name', 'Domain', 'Description', 'Retention period', 'Data Controller', 'User Privacy & GDPR Rights Portals', 'Wildcard match']
    valid_categories = ['Functional','Personalization','Analytics', 'Marketing', 'Security']
    
    # Check if CSV has valid structure and contains necessary columns
    if not set(columns).issubset(df.columns):
        print("::error file=open-cookie-database.csv,line=1,col=1::CSV structure is not valid.")
        return False

 # Check if 'Category' column contains only valid values
    if not df['Category'].isin(valid_categories).all():
        print("::error file=open-cookie-database.csv,line=1,col=1::'Category' column must contain only these values: " + ', '.join(valid_categories))
        invalid_categories = df[~df['Category'].isin(valid_categories)]['Category']
        print("Invalid categories are:")
        print(invalid_categories)
        return False

    # Check if 'ID' column contains unique UUID values
    if not (df['ID'].apply(validate_uuid).all() and df['ID'].is_unique):
        print("::error file=open-cookie-database.csv,line=1,col=1::'ID' column must contain unique UUID values.")
        
        non_unique_ids = df[df.duplicated('ID', keep=False)][['ID', 'Cookie / Data Key name']]
        print("Non-unique IDs and corresponding cookie names are:")
        print(non_unique_ids)
        return False

    # Check if 'Cookie / Data Key name' column contains unique values
    if not df['Cookie / Data Key name'].is_unique:
        non_unique_cookies = df[df.duplicated('Cookie / Data Key name', keep=False)]['Cookie / Data Key name']
        non_unique_cookies_str = ', '.join(non_unique_cookies)
        print(f"::warning file=open-cookie-database.csv,line=1,col=1::'Cookie / Data Key name' contains non-unique values: {non_unique_cookies_str}. Please check for duplicates.")

    print("CSV file is valid.")
    return True

validate_csv('open-cookie-database.csv')
