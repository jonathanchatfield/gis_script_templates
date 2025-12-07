import subprocess
import os

# ==========================================
#        CONFIGURATION SECTION
#      (Customize this for each job)
# ==========================================

# 1. INPUT FILE
# Full path to the .shp file you want to import.
# Example: "/Users/jonathan/Downloads/rivers/rivers.shp"
INPUT_SHAPEFILE = r"[[FULL_PATH_TO_YOUR_SHAPEFILE.shp]]"

# 2. DATABASE DETAILS
# Your local PostGIS credentials.
DB_Host = "[[localhost]]"
DB_NAME = "[[YOUR_DATABASE_NAME]]"      # e.g. "jonathan"
DB_USER = "[[YOUR_USERNAME]]"           # e.g. "jonathan"
DB_PASSWORD = "[[YOUR_PASSWORD]]"       # Leave empty "" if using trusted local auth

# 3. OUTPUT TABLE DETAILS
# What do you want the table to be named in PostGIS?
# Example: "indian_rivers"
TABLE_NAME = "[[DESIRED_TABLE_NAME]]"

# 4. ROW FILTER (SQL WHERE Clause)
# Filter rows *before* importing. Use "1=1" to import everything.
# Example: "ADM0NAME = 'India'"
WHERE_FILTER = "[[SQL_FILTER_CONDITION]]" 

# 5. COLUMN FILTER (Select Attributes)
# Comma-separated list of columns to keep. 
# WARNING: Must match the exact headers in the source file.
# Example: "NAME,POP_MAX,LATITUDE"
COLUMNS_TO_KEEP = "[[LIST_OF_COLUMNS_TO_KEEP]]"


# ==========================================
#          THE ENGINE (Do not edit)
# ==========================================

def run_import():
    # Construct the connection string for ogr2ogr
    connection_string = f"PG:host={DB_Host} PG:dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
# db_connection = "PG:host=localhost dbname=jonathan user=jonathan"
    # Build the command list
    # We use a list instead of a string to safely handle spaces in file paths
    cmd = [
        "ogr2ogr",                      # The tool
        "-f", "PostgreSQL",             # Target format
        connection_string,              # Destination DB
        INPUT_SHAPEFILE,                # Source File
        "-nln", TABLE_NAME,             # New Layer Name
        "-overwrite",                   # Nuke existing table if it matches name
        "-lco", "GEOMETRY_NAME=geom",   # Standardize geometry column name
        "-progress",                    # Show a progress bar in terminal
        
        # Apply the filters defined above
        "-where", WHERE_FILTER,
        "-select", COLUMNS_TO_KEEP
    ]

    print(f"🚀 Starting import for: {os.path.basename(INPUT_SHAPEFILE)}")
    print(f"➡️  Target Table: {TABLE_NAME}")

    try:
        # Run the command and wait for it to finish
        subprocess.check_call(cmd)
        print(f"✅ Success! Data imported into table '{TABLE_NAME}'.")

    except subprocess.CalledProcessError as e:
        print("\n❌ IMPORT FAILED.")
        print(f"   Exit Code: {e.returncode}")
        print("   Tip: Check your column names and file path.")

    except FileNotFoundError:
        print("\n❌ SYSTEM ERROR: 'ogr2ogr' tool not found.")
        print("   Make sure you are in your Conda environment with GDAL installed.")

if __name__ == "__main__":
    run_import()