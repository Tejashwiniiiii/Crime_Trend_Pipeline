
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: load.py
# PURPOSE: Load transformed data into PostgreSQL
# ==========================================

import pandas as pd
from sqlalchemy import create_engine, text

from config import PROCESSED_DATA_DIR, DATABASE_URL


def load_crime_data():

    print("\nSTARTING DATA LOADING...")

    # Step 1: Read transformed CSV file
    input_file = PROCESSED_DATA_DIR / "crime_transformed.csv"

    df = pd.read_csv(input_file)

    print("Step 1 passed: Transformed data loaded.")
    print("Total records:", len(df))

    # Step 2: Create PostgreSQL connection
    engine = create_engine(DATABASE_URL)

    print("\nStep 2 passed: PostgreSQL connection created.")

    # Step 3: Load data into PostgreSQL
    df.to_sql(
        name="crime_data",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi"
    )

    print("Step 3 passed: Data inserted into PostgreSQL.")

    # Step 4: Verify loaded records
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT COUNT(*) FROM crime_data")
        )

        total_records = result.scalar()

    print("\nStep 4 passed: Database records verified.")
    print("Total records in PostgreSQL:", total_records)

    # Step 5: Display sample records
    with engine.connect() as connection:

        preview = pd.read_sql(
            text("SELECT * FROM crime_data LIMIT 5"),
            connection
        )

    print("\nDATABASE DATA PREVIEW:")
    print(preview)

    engine.dispose()

    print("\nDATA LOADING COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":

    load_crime_data()
