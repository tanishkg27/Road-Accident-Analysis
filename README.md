# Road Accident Analysis Dashboard

A browser-based road accident data analysis application built with Python, Streamlit, Pandas and Plotly.

The interface uses a calm cream, sage and burgundy palette and includes responsive analysis views for accident trends, locations and dataset exploration.

## Dashboard features

- **Dashboard:** filtered accident, casualty and fatality totals, key charts and dataset-based insights.
- **Accident Analysis:** year, month, day-of-week, vehicle, severity and casualty/fatality comparisons.
- **Location Analysis:** top accident-prone locations with a matching summary table.
- **Data Explorer:** search, filtered CSV download, missing-value counts and statistical summary.
- **Project Information:** scope, technology and interpretation notes.

Year, month, location, vehicle type and severity filters are available in the sidebar. Charts and insights use the selected records. Missing or empty source columns are handled with informative empty states rather than fabricated values.

## Project structure

```text
Road_Accident_Analysis/
├── app.py
├── data.py
├── analysis.py
├── requirements.txt
├── README.md
└── data/
    └── accident_data.csv
```

## Setup on Windows

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open the terminal.
4. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

7. Open the local browser address shown in the terminal (normally http://localhost:8501).

## Dataset

Upload a CSV using the sidebar, or place a CSV named `accident_data.csv` in the `data` folder.

The application recognizes common column names such as date, year, location, vehicle type, accident severity, weather conditions, casualties and fatalities. Charts that require unavailable columns will show a helpful message.

**Important:** The total accident count is the number of rows. Use a dataset where each row represents one accident. A fatal accident count is not the same as the number of people killed.

## Suggested dataset sources

- Government of India Open Government Data: https://www.data.gov.in/
- Kaggle: https://www.kaggle.com/datasets/tsiaras/uk-road-safety-accidents-and-vehicles

Use the dataset's license and attribution requirements when submitting or publishing your project.
