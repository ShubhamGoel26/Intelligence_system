import pandas as pd

def clean_email(text):
    """
    Convert formats like:
    'Email : abc[at]gmail[dot]com' → 'abc@gmail.com'
    """
    if not isinstance(text, str):
        return None

    text = text.lower()

    email = (
        text.replace("email :", "")
            .replace("email:", "")
            .replace("[at]", "@")
            .replace("[dot]", ".")
            .strip()
    )

    return email if "@" in email else None


def read_companies(file_path: str):
    """
    Reads Excel file with no headers and extracts:
    - Company name
    - Location
    - Email (optional)
    """

    # ✅ Read without assuming header
    df = pd.read_excel(file_path, header=None)

    companies = []

    for _, row in df.iterrows():

        # 🔹 Extract by index (based on your sheet)
        name = row[3] if len(row) > 2 else None
        location = row[2] if len(row) > 1 else ""
        raw_email = row[4] if len(row) > 3 else None

        # ❌ Skip invalid rows
        if pd.isna(name):
            continue

        # ✅ Clean values
        name = str(name).strip()
        location = str(location).strip() if not pd.isna(location) else ""
        email = clean_email(raw_email)

        companies.append({
            "name": name,
            "location": location,
            "email": email
        })

    return companies
