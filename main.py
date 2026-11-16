
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: main.py
# PURPOSE: Run the complete crime data pipeline
# ==========================================

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

from extract import extract_crime_data
from validate import validate_crime_data
from transform import transform_crime_data
from load import load_crime_data


def run_pipeline():

    print("\n========================================")
    print("   CRIME TREND DATA PIPELINE STARTED")
    print("========================================")

    # STEP 1: EXTRACT
    raw_data = extract_crime_data()

    # STEP 2: VALIDATE
    validated_data = validate_crime_data(raw_data)

    validated_file = RAW_DATA_DIR / "crime_validated.csv"
    validated_data.to_csv(validated_file, index=False)

    print("\nValidated data saved:", validated_file)

    # STEP 3: TRANSFORM
    transformed_data = transform_crime_data(validated_data)

    transformed_file = PROCESSED_DATA_DIR / "crime_transformed.csv"
    transformed_data.to_csv(transformed_file, index=False)

    print("\nTransformed data saved:", transformed_file)

    # STEP 4: LOAD
    load_crime_data()

    print("\n========================================")
    print("   COMPLETE PIPELINE EXECUTED SUCCESSFULLY")
    print("========================================")


if __name__ == "__main__":
    run_pipeline()
