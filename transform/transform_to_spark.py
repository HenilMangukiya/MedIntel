import json
import pandas as pd
from pyspark.sql import SparkSession
import os

def transform_json_to_spark(indicator_code):
    # Path to raw JSON
    path = f"data/raw/{indicator_code.lower()}_raw.json"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw file not found at: {path}")

    # Load raw JSON
    with open(path, "r") as file:
        raw_data = json.load(file)

    # Normalize using Pandas
    df = pd.json_normalize(raw_data)

    # Select and rename relevant columns
    df = df[["SpatialDim", "TimeDim", "Value", "IndicatorCode"]]
    df.columns = ["Country", "Year", "Value", "Indicator"]

    # Convert datatypes
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Country", "Year", "Value"])

    # Start Spark session
    spark = SparkSession.builder \
        .appName("MedIntelTransform") \
        .getOrCreate()

    # Convert to Spark DataFrame
    spark_df = spark.createDataFrame(df)

    # Preview
    spark_df.show(10)

    return spark_df

# Example usage
if __name__ == "__main__":
    indicator = input("Enter indicator code (e.g., TUB_CDR): ")
    transform_json_to_spark(indicator)
