import os
import pandas as pd
import streamlit as st

COLUMN_ALIASES = {
    "date": ["date", "accident_date", "accident date", "date_of_accident", "c_date"],
    "year": ["year", "accident_year", "accident year"],
    "month": ["month", "accident_month"],
    "day": ["day_of_week", "day of week", "weekday"],
    "location": ["location", "local_authority_district", "local_authority", "city", "district", "state", "accident_location"],
    "vehicle": ["vehicle_type", "vehicle type", "vehicle", "vehicle_category"],
    "severity": ["accident_severity", "accident severity", "severity"],
    "weather": ["weather_conditions", "weather conditions", "weather"],
    "casualties": ["number_of_casualties", "number of casualties", "casualties", "total_casualties"],
    "fatalities": ["fatalities", "number_of_fatalities", "number of fatalities", "persons_killed", "killed"],
    "time": ["time", "accident_time", "accident time"],
}

def clean_column_names(df):
    df.columns = (
        df.columns.astype(str).str.strip().str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df

def standardize_columns(df):
    df = clean_column_names(df)
    for standard, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias = alias.lower().replace(" ", "_")
            if alias in df.columns:
                if standard not in df.columns:
                    df.rename(columns={alias: standard}, inplace=True)
                break
    return df

def load_data(uploaded_file=None):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "accident_data.csv")
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return None
            df = pd.read_csv(file_path)

        if df.empty:
            return None

        df = standardize_columns(df)

        if "date" in df.columns:
            date_text = df["date"].astype("string").str.strip()
            iso_dates = date_text.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}", na=False)
            parsed_dates = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
            if iso_dates.any():
                parsed_dates.loc[iso_dates] = pd.to_datetime(
                    df.loc[iso_dates, "date"], errors="coerce", dayfirst=False
                )
            non_iso_dates = df["date"].notna() & ~iso_dates
            if non_iso_dates.any():
                parsed_dates.loc[non_iso_dates] = pd.to_datetime(
                    df.loc[non_iso_dates, "date"], errors="coerce", dayfirst=True
                )
                unparsed_non_iso = parsed_dates.isna() & non_iso_dates
                if unparsed_non_iso.any():
                    parsed_dates.loc[unparsed_non_iso] = pd.to_datetime(
                        df.loc[unparsed_non_iso, "date"], errors="coerce", dayfirst=True
                    )
            df["date"] = parsed_dates
            if "year" not in df.columns:
                df["year"] = df["date"].dt.year
            if "month" not in df.columns:
                df["month"] = df["date"].dt.month_name()
            if "day" not in df.columns:
                df["day"] = df["date"].dt.day_name()

        for col in ["year", "casualties", "fatalities"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    except (OSError, UnicodeDecodeError, ValueError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        st.error(f"Error loading dataset: {e}")
        return None
