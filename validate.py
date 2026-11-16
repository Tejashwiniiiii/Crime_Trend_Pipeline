
import pandas as pd

from config import RAW_DATA_DIR


def validate_crime_data(df):

    print("\nSTARTING DATA VALIDATION...")

    required_columns = [
        "date_time",
        "id",
        "type",
        "subtype",
        "location",
        "description",
        "last_updated"
    ]

    # Check 1: Verify required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    print("Check 1 passed: All required columns are available.")

    # Check 2: Check empty dataset
    if df.empty:
        raise ValueError("Dataset is empty.")

    print("Check 2 passed: Dataset contains records.")

    # Check 3: Check duplicate IDs
    duplicate_count = df["id"].duplicated().sum()

    print("Duplicate records found:", duplicate_count)

    # Check 4: Check missing values
    print("\nMissing values in each column:")
    print(df[required_columns].isnull().sum())

    # Handle missing descriptions
    df["description"] = df["description"].fillna("Not Available")

    print("\nMissing values after handling:")
    print(df[required_columns].isnull().sum())

    # Check 5: Validate date format
    valid_dates = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    invalid_dates = valid_dates.isnull().sum()

    print("\nInvalid date records:", invalid_dates)

    if invalid_dates > 0:
        raise ValueError("Dataset contains invalid date records.")

    print("\nDATA VALIDATION COMPLETED!")

    return df


if __name__ == "__main__":

    # Read raw data
    input_file = RAW_DATA_DIR / "crime_raw.csv"

    crime_data = pd.read_csv(input_file)

    # Validate data
    validated_data = validate_crime_data(crime_data)

    # Save validated data
    output_file = RAW_DATA_DIR / "crime_validated.csv"

    validated_data.to_csv(output_file, index=False)

    print("\nVALIDATED DATA SAVED SUCCESSFULLY!")
    print("File location:", output_file)

    # Display preview
    print("\nVALIDATED DATA PREVIEW:")
    print(validated_data.head())
