
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: transform.py
# PURPOSE: Clean and transform crime data
# ==========================================

import pandas as pd

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def transform_crime_data(df):

    print("\nSTARTING DATA TRANSFORMATION...")

    # Check 1: Convert date_time into datetime format
    df["date_time"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    print("Check 1 passed: Date and time converted.")

    # Check 2: Extract date-related information
    df["year"] = df["date_time"].dt.year
    df["month"] = df["date_time"].dt.month
    df["day"] = df["date_time"].dt.day
    df["hour"] = df["date_time"].dt.hour
    df["day_name"] = df["date_time"].dt.day_name()

    print("Check 2 passed: Year, month, day, hour and day name extracted.")

    # Check 3: Clean text columns
    text_columns = [
        "type",
        "subtype",
        "location",
        "description"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("Not Available")
        df[column] = df[column].astype(str).str.strip()

    print("Check 3 passed: Text columns cleaned.")

    # Check 4: Create time period column
    def get_time_period(hour):

        if 5 <= hour < 12:
            return "Morning"

        elif 12 <= hour < 17:
            return "Afternoon"

        elif 17 <= hour < 21:
            return "Evening"

        else:
            return "Night"

    df["time_period"] = df["hour"].apply(get_time_period)

    print("Check 4 passed: Time periods created.")

    # Check 5: Remove invalid date records
    df = df.dropna(subset=["date_time"])

    print("Check 5 passed: Invalid date records removed.")

    print("\nDATA TRANSFORMATION COMPLETED!")

    return df


if __name__ == "__main__":

    # Read validated dataset
    input_file = RAW_DATA_DIR / "crime_validated.csv"

    crime_data = pd.read_csv(input_file)

    # Transform data
    transformed_data = transform_crime_data(crime_data)

    # Save transformed dataset
    output_file = PROCESSED_DATA_DIR / "crime_transformed.csv"

    transformed_data.to_csv(output_file, index=False)

    print("\nTRANSFORMED DATA SAVED SUCCESSFULLY!")
    print("File location:", output_file)

    # Display final preview
    print("\nTRANSFORMED DATA PREVIEW:")
    print(transformed_data.head())

    print("\nTotal records after transformation:",
          len(transformed_data))
