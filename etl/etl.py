import requests
import pandas as pd
import logging
import time

from models import MarketData
from db import engine


# ==========================
# Logging Configuration
# ==========================

logging.basicConfig(
    filename="../logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================
# VWAP Calculation
# ==========================

def calculate_vwap(records):

    df = pd.DataFrame(records)

    vwap_df = (
        df.groupby("instrument_id")
        .apply(
            lambda x:
            (x["price"] * x["volume"]).sum()
            / x["volume"].sum(),
            include_groups=False
        )
        .reset_index(name="vwap")
    )

    df = df.merge(
        vwap_df,
        on="instrument_id"
    )

    return df


# ==========================
# Outlier Detection
# ==========================

def detect_outliers(df):

    avg_price_df = (
        df.groupby("instrument_id")["price"]
        .mean()
        .reset_index(name="avg_price")
    )

    df = df.merge(
        avg_price_df,
        on="instrument_id"
    )

    df["is_outlier"] = (
        abs(df["price"] - df["avg_price"])
        >
        (df["avg_price"] * 0.15)
    )

    df.drop(
        columns=["avg_price"],
        inplace=True
    )

    return df


# ==========================
# Load to PostgreSQL
# ==========================

def load_data(df):

    try:

        df.to_sql(
            "market_data",
            engine,
            if_exists="append",
            index=False
        )

        print(f"{len(df)} records inserted")

    except Exception as e:

        print(f"Database Error: {e}")


# ==========================
# Main ETL Process
# ==========================

def main():

    start_time = time.time()

    API_URL = "http://localhost:8000/v1/market-data"

    valid_records = []
    dropped = 0

    try:

        response = requests.get(
            API_URL,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        for record in data:

            try:

                validated = MarketData(**record)

                valid_records.append(
                    validated.model_dump()
                )

            except Exception:

                dropped += 1

        print(f"Valid Records: {len(valid_records)}")
        print(f"Dropped Records: {dropped}")

        if len(valid_records) == 0:

            print("No valid records found")
            return

        # VWAP
        df = calculate_vwap(valid_records)

        # Outlier Detection
        df = detect_outliers(df)

        print("\nTransformed Data:")
        print(df.head())

        # Load into DB
        load_data(df)

        # Execution Time
        execution_time = round(
            time.time() - start_time,
            2
        )

        # Logging
        logging.info(
            f"Records Processed: {len(valid_records)}"
        )

        logging.info(
            f"Records Dropped: {dropped}"
        )

        logging.info(
            f"Execution Time: {execution_time} seconds"
        )

        # Summary
        print("\nETL Summary")
        print(
            f"Records Processed: {len(valid_records)}"
        )
        print(
            f"Records Dropped: {dropped}"
        )
        print(
            f"Execution Time: {execution_time} sec"
        )

    except requests.exceptions.Timeout:

        print("Timeout Error")

    except requests.exceptions.HTTPError as e:

        print(f"HTTP Error: {e}")

    except Exception as e:

        print(f"Unexpected Error: {e}")


# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":
    main()