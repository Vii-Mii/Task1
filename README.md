# ETL Pipeline for Sales Data

This project implements an ETL (Extract, Transform, Load) pipeline that processes and transforms sales data from two regions (A and B), applies necessary business rules, and loads the results into an SQLite database.

## Requirements

Before running the script, make sure you have the following:

- Python 3.6 or higher
- `pandas` library
- `sqlite3` (comes pre-installed with Python)
- `openpyxl` library (for reading Excel files)

### Install Required Libraries

To install the necessary Python libraries, use the following command:

```bash
pip install pandas openpyxl
python ETL.py
