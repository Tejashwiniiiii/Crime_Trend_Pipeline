
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: extract.py
# PURPOSE: Extract crime data from Socrata API
# ==========================================

import pandas as pd
from sodapy import Socrata

from config import (
    SOCRATA_DOMAIN,
    DATASET_ID,
    SOCRATA_APP_TOKEN,
    RAW_DATA_DIR
)

# Number of records to download
LIMIT = 5000


def extract_crime_data():

    print("\nSTARTING DATA EXTRACTION...")
    
    try:
        # Connect to Cambridge Police dataset
        client = Socrata(
            SOCRATA_DOMAIN,
            SOCRATA_APP_TOKEN,
            timeout=60
        )

        # Download records
        records = client.get(
            DATASET_ID,
            limit=LIMIT,
            order="date_time DESC"
        )

        # Convert records into DataFrame
        df = pd.DataFrame.from_records(records)

        if df.empty:
            raise ValueError("No records received from API.")

        # Save raw data
        output_file = RAW_DATA_DIR / "crime_raw.csv"

        df.to_csv(output_file, index=False)

        print("DATA EXTRACTION SUCCESSFUL!")
        print("Total records downloaded:", len(df))
        print("Raw data saved at:", output_file)

        return df

    except Exception as error:
        print("DATA EXTRACTION FAILED!")
        print("Error:", error)
        raise

    finally:
        if "client" in locals():
            client.close()


# Run extraction independently
if __name__ == "__main__":
    crime_data = extract_crime_data()

    print("\nFIRST FIVE RECORDS:")
    print(crime_data.head())

    print("\nAVAILABLE COLUMNS:")
    print(crime_data.columns.tolist())
