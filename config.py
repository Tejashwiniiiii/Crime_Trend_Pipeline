
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: config.py
# PURPOSE: Manage local, Docker and cloud configuration
# ==========================================

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# 1. Identify the main project directory
BASE_DIR = Path(__file__).resolve().parent

# 2. Load local environment variables
# Do not overwrite environment variables provided by Render
load_dotenv(BASE_DIR / ".env", override=False)

# 3. Crime dataset configuration
SOCRATA_DOMAIN = "data.cambridgema.gov"
DATASET_ID = "3gki-wyrb"

SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN") or None

# 4. Define project folder paths
DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"

# 5. Create folders if they do not exist
for folder in [RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# 6. PostgreSQL configuration for local/Docker use
POSTGRES_USER = os.getenv("POSTGRES_USER", "crime_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "change_me")
POSTGRES_DB = os.getenv("POSTGRES_DB", "cpd_db")

# Use localhost for normal local execution.
# For Docker on Windows, set POSTGRES_HOST=host.docker.internal
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")

POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

# 7. Database connection configuration
# Render DATABASE_URL takes priority when provided.

RENDER_DATABASE_URL = os.getenv("DATABASE_URL")

if RENDER_DATABASE_URL:

    # Normalize PostgreSQL URL for SQLAlchemy + psycopg2
    if RENDER_DATABASE_URL.startswith("postgres://"):
        RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )

    elif RENDER_DATABASE_URL.startswith("postgresql://"):
        RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1
        )

    DATABASE_URL = RENDER_DATABASE_URL

else:

    # Local PostgreSQL connection
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )

# 8. Display basic configuration information
if __name__ == "__main__":

    print("PROJECT CONFIGURATION LOADED SUCCESSFULLY!")
    print("------------------------------------------")

    print("Project Directory:", BASE_DIR)
    print("Dataset Domain:", SOCRATA_DOMAIN)
    print("Dataset ID:", DATASET_ID)

    print("Raw Data Folder:", RAW_DATA_DIR)
    print("Processed Data Folder:", PROCESSED_DATA_DIR)

    print("Database Name:", POSTGRES_DB)

    if RENDER_DATABASE_URL:
        print("Database Mode: Cloud")
    else:
        print("Database Mode: Local/Docker")
        print("Database Host:", POSTGRES_HOST)
        print("Database Port:", POSTGRES_PORT)

    print("Configuration is ready!")
