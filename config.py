
# ==========================================
# PROJECT: DATA PIPELINE TO MONITOR LOCAL CRIME TRENDS
# FILE: config.py
# PURPOSE: Manage project configuration
# ==========================================

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# 1. Identify the main project directory
BASE_DIR = Path(__file__).resolve().parent

# 2. Load environment variables from .env
load_dotenv(BASE_DIR / ".env", override=True)

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

# 6. PostgreSQL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "crime_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "change_me")
POSTGRES_DB = os.getenv("POSTGRES_DB", "cpd_db")

# Docker-compatible PostgreSQL host
POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "host.docker.internal"
)

POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

# 7. Create database connection URL safely
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
    print("Database Host:", POSTGRES_HOST)
    print("Database Port:", POSTGRES_PORT)
    print("Configuration is ready!")
