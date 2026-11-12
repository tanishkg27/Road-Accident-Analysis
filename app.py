import html

import pandas as pd
import streamlit as st

from analysis import (
    create_bar_chart,
    create_casualties_chart,
    create_line_chart,
    create_pie_chart,
    create_top_locations_chart,
    get_insights,
    get_top_location,
)
from data import load_data

st.set_page_config(
    page_title="Road Accident Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {
        --sage: #A3A99B;
        --cream: #F3EBDD;
        --burgundy: #702C3B;
        --deep: #4A1F2B;
        --white: #FAF8F3;
        --muted: #77796F;
    }
    .stApp {
        background: var(--cream);
        color: var(--muted);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(243, 235, 221, .92); }
    [data-testid="stSidebar"] {
        background: var(--deep);
        border-right: 1px solid rgba(250,248,243,.12);
    }
    [data-testid="stSidebar"] > div:first-child { background: var(--deep); }
    [data-testid="stSidebar"] * { color: var(--white); }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: rgba(250,248,243,.08);
        border: 1px dashed rgba(250,248,243,.35);
        border-radius: 12px;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
        background: rgba(250,248,243,.10);
        border-color: rgba(250,248,243,.22);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 10px;
        border-radius: 10px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: rgba(250,248,243,.14);
    }
    h1, h2, h3, h4 {
        color: var(--deep) !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        letter-spacing: -.025em;
    }
    p, label, [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0 20px;
        border-bottom: 1px solid rgba(250,248,243,.16);
        margin-bottom: 20px;
    }
    .brand-mark {
        width: 42px;
        height: 42px;
        border-radius: 13px;
        display: grid;
        place-items: center;
        background: var(--burgundy);
        font-size: 21px;
    }
    .brand-name { font-size: 15px; font-weight: 700; line-height: 1.2; }
    .brand-kicker {
        color: rgba(250,248,243,.65);
        font-size: 10px;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .eyebrow {
        color: var(--burgundy);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .page-title {
        color: var(--deep);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 700;
        line-height: 1.08;
        letter-spacing: -.035em;
        margin: 0;
    }
    .page-subtitle { color: var(--muted); font-size: 15px; margin-top: 8px; }
    .dataset-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(112,44,59,.08);
        color: var(--deep);
        border: 1px solid rgba(112,44,59,.13);
        border-radius: 999px;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 18px;
    }
    .metric-card, .panel, .insight-card {
        background: var(--white);
        border: 1px solid rgba(74,31,43,.07);
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(74,31,43,.055);
    }
    .metric-grid, .insight-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 14px;
    }
    .metric-card {
        min-height: 154px;
        padding: 19px 20px;
        border-top: 3px solid var(--burgundy);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .metric-card:hover, .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(74,31,43,.09);
    }
    .metric-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
    }
    .metric-icon {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        background: rgba(112,44,59,.09);
        border-radius: 11px;
        font-size: 17px;
    }
    .metric-value {
        color: var(--deep);
        font-size: clamp(25px, 2.2vw, 34px);
        font-weight: 700;
        line-height: 1.15;
        margin-top: 15px;
        overflow-wrap: anywhere;
    }
    .metric-value.location { font-size: clamp(18px, 1.8vw, 25px); }
    .metric-note { color: var(--muted); font-size: 11px; margin-top: 7px; }
    .section-label {
        color: var(--deep);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 22px;
        font-weight: 700;
        margin: 25px 0 4px;
    }
    .section-note { color: var(--muted); font-size: 13px; margin: 0 0 12px; }
    .insight-card {
        padding: 18px 19px;
        min-height: 112px;
        border-left: 4px solid var(--sage);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .insight-grid { grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); }
    .insight-label {
        color: var(--muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .insight-value { color: var(--deep); font-size: 16px; font-weight: 700; }
    .project-card {
        background: var(--white);
        border-radius: 18px;
        border: 1px solid rgba(74,31,43,.07);
        padding: 22px;
        height: 100%;
    }
    div.stButton > button, div.stDownloadButton > button {
        background: var(--burgundy);
        color: var(--white);
        border: 1px solid var(--burgundy);
        border-radius: 10px;
        font-weight: 600;
        transition: background .15s ease, transform .15s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: var(--deep);
        color: var(--white);
        border-color: var(--deep);
        transform: translateY(-1px);
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid rgba(74,31,43,.09);
        border-radius: 14px;
        overflow: hidden;
    }
    [data-testid="stMetric"] {
        background: var(--white);
        border: 1px solid rgba(74,31,43,.07);
        border-radius: 14px;
        padding: 14px 16px;
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--deep); }
    [data-testid="stAlert"] { border-radius: 12px; }
    hr { border-color: rgba(74,31,43,.12); }
    @media (max-width: 700px) {
        .block-container { padding: 1.2rem 1rem 2rem; }
        .metric-card { min-height: 138px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGE_ICONS = {
    "Dashboard": "⌂",
    "Accident Analysis": "◷",
    "Location Analysis": "⌖",
    "Data Explorer": "▤",
    "Project Information": "ⓘ",
}

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">🚦</div>
            <div>
                <div class="brand-name">Road Safety</div>
                <div class="brand-kicker">Intelligence platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**WORKSPACE**")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Accident Analysis", "Location Analysis", "Data Explorer", "Project Information"],
        format_func=lambda item: f"{PAGE_ICONS[item]}  {item}",
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**DATASET**")
    uploaded_file = st.file_uploader("Upload an accident CSV", type=["csv"], label_visibility="collapsed")
    st.caption("Upload a CSV to explore your own accident records.")

df = load_data(uploaded_file)
if df is None:
    st.markdown('<div class="eyebrow">Road safety analytics</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Road Accident Intelligence</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Data-driven insights for safer roads.</p>',
        unsafe_allow_html=True,
    )
    st.warning("No dataset found. Upload a CSV file or add data/accident_data.csv.")
    st.info("For accurate accident counts, use a dataset where each row represents one accident.")
    st.stop()

source_name = uploaded_file.name if uploaded_file is not None else "data/accident_data.csv"
filtered_df = df.copy()

with st.sidebar:
    st.markdown("---")
    st.markdown("**FILTERS**")

    def add_filter(column, label, order=None):
        global filtered_df
        if column not in filtered_df.columns:
            return
        values = df[column].dropna().astype(str).unique().tolist()
        if order:
            ranks = {value.lower(): index for index, value in enumerate(order)}
            values.sort(key=lambda value: (ranks.get(value.lower(), len(ranks)), value.lower()))
        else:
            values.sort(key=lambda value: (not value.isdigit(), int(value) if value.isdigit() else value.lower()))
        if values:
            selected = st.multiselect(label, values, default=values, key=f"filter_{column}")
            filtered_df = filtered_df[filtered_df[column].astype(str).isin(selected)]

    add_filter("year", "Year")
    add_filter(
        "month",
        "Month",
        ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"],
    )
    add_filter("location", "Location")
    add_filter("vehicle", "Vehicle type")
    add_filter("severity", "Accident severity")
    st.markdown("---")
    st.markdown(
        '<div style="font-size:11px;color:rgba(250,248,243,.66);line-height:1.6">'
        '<b>PROJECT</b><br>Road Accident Analysis<br>Python · Streamlit · Plotly</div>',
        unsafe_allow_html=True,
    )


def safe_text(value):
    return html.escape(str(value))


def show_header(title, subtitle, eyebrow="ROAD SAFETY ANALYTICS"):
    st.markdown(f'<div class="eyebrow">{safe_text(eyebrow)}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="page-title">{safe_text(title)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{safe_text(subtitle)}</div>', unsafe_allow_html=True)


def show_chart(fig, message="This chart needs a populated, compatible column in the selected dataset."):
    if fig is not None:
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False, "responsive": True})
    else:
        st.info(message)


def metric_value(column):
    if column not in filtered_df.columns:
        return "N/A"
    value = pd.to_numeric(filtered_df[column], errors="coerce").sum(min_count=1)
    return f"{int(value):,}" if pd.notna(value) else "N/A"


def metric_card(label, value, note, icon, location=False):
    value_class = "metric-value location" if location else "metric-value"
    return (
        '<div class="metric-card">'
        f'<div class="metric-head"><span>{safe_text(label)}</span>'
        f'<span class="metric-icon">{safe_text(icon)}</span></div>'
        f'<div class="{value_class}">{safe_text(value)}</div>'
        f'<div class="metric-note">{safe_text(note)}</div>'
        "</div>"
    )


def section_heading(title, note=""):
    st.markdown(f'<div class="section-label">{safe_text(title)}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="section-note">{safe_text(note)}</div>', unsafe_allow_html=True)


def show_insights():
    insights = get_insights(filtered_df)
    if not insights:
        st.info("Not enough populated fields in the current selection to generate data-backed observations.")
        return
    cards = []
    for insight in insights:
        label, separator, value = insight.partition(": ")
        value = value.rstrip(".") if separator else insight
        cards.append(
            '<div class="insight-card">'
            f'<div class="insight-label">{safe_text(label)}</div>'
            f'<div class="insight-value">{safe_text(value)}</div>'
            "</div>"
        )
    st.markdown(f'<div class="insight-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


if page == "Dashboard":
    show_header("Road Accident Intelligence", "Data-driven insights for safer roads.")
    st.markdown(
        f'<div class="dataset-pill">◉ &nbsp;{safe_text(source_name)}'
        f' &nbsp;·&nbsp; {len(df):,} records &nbsp;·&nbsp; {len(filtered_df):,} in current view</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    fatalities = metric_value("fatalities")
    if fatalities == "N/A" and "severity" in filtered_df.columns:
        severity = filtered_df["severity"].astype(str).str.strip().str.lower()
        fatal_count = int(severity.isin(["fatal", "1"]).sum())
        fatalities = f"{fatal_count:,} fatal accidents"

    location = get_top_location(filtered_df)
    cards = [
        ("Total Accidents", f"{len(filtered_df):,}", "Recorded rows in selected view", "▥", False),
        ("Total Casualties", metric_value("casualties"), "People recorded as injured or affected", "＋", False),
        ("Total Fatalities", fatalities, "People killed, when available", "✦", False),
        ("Most Accident-Prone Location", location, "Highest recorded accident frequency", "⌖", True),
    ]
    metric_markup = "".join(metric_card(*card) for card in cards)
    st.markdown(f'<div class="metric-grid">{metric_markup}</div>', unsafe_allow_html=True)

    section_heading("Accident patterns", "Use the filters to compare the records that matter to you.")
    left, right = st.columns(2)
    with left:
        show_chart(create_line_chart(filtered_df, "year", "Accidents by Year"))
    with right:
        show_chart(create_pie_chart(filtered_df, "severity", "Accident Severity Distribution"))
    left, right = st.columns(2)
    with left:
        show_chart(create_bar_chart(filtered_df, "vehicle", "Accidents by Vehicle Type"))
    with right:
        show_chart(create_bar_chart(filtered_df, "weather", "Accidents by Weather Conditions"))

    section_heading("Automatic insights", "Observations are calculated from the filtered dataset.")
    show_insights()

elif page == "Accident Analysis":
    show_header("Accident Analysis", "Explore timing, severity and the people affected.")
    left, right = st.columns(2)
    with left:
        show_chart(create_line_chart(filtered_df, "year", "Accidents by Year"))
    with right:
        show_chart(create_bar_chart(filtered_df, "month", "Accidents by Month"))
    left, right = st.columns(2)
    with left:
        show_chart(create_bar_chart(filtered_df, "day", "Accidents by Day of Week"))
    with right:
        show_chart(create_pie_chart(filtered_df, "severity", "Accident Severity Distribution"))
    left, right = st.columns(2)
    with left:
        show_chart(create_bar_chart(filtered_df, "vehicle", "Accidents by Vehicle Type"))
    with right:
        show_chart(create_casualties_chart(filtered_df))

elif page == "Location Analysis":
    show_header("Location Analysis", "Understand where recorded accidents are most frequent.")
    chart = create_top_locations_chart(filtered_df)
    if "location" not in filtered_df.columns:
        st.warning("The location column is not available in this dataset.")
    elif filtered_df.empty or filtered_df["location"].dropna().empty:
        st.info("No location values are available in the current selection.")
    else:
        show_chart(chart)
        location_data = (
            filtered_df["location"].dropna().astype(str).value_counts()
            .head(10).rename_axis("Location").reset_index(name="Accidents")
        )
        st.dataframe(location_data, width="stretch", hide_index=True)

elif page == "Data Explorer":
    show_header("Data Explorer", "Search, inspect and export the records behind the analysis.")
    search = st.text_input("Search across the selected records", placeholder="Search any column or value...")
    explorer_df = filtered_df.copy()
    if search:
        mask = explorer_df.astype(str).apply(
            lambda column: column.str.contains(search, case=False, na=False, regex=False)
        ).any(axis=1)
        explorer_df = explorer_df[mask]

    section_heading("Accident dataset", f"Showing {len(explorer_df):,} matching rows from the filtered selection.")
    st.dataframe(explorer_df, width="stretch", height=420, hide_index=True)
    st.download_button(
        "Download filtered CSV",
        explorer_df.to_csv(index=False).encode("utf-8"),
        "filtered_accident_data.csv",
        "text/csv",
    )

    section_heading("Dataset at a glance")
    info_columns = st.columns(3)
    info_columns[0].metric("Total rows", f"{len(df):,}")
    info_columns[1].metric("Total columns", len(df.columns))
    info_columns[2].metric("Filtered rows", f"{len(explorer_df):,}")

    left, right = st.columns([1, 1.5])
    with left:
        section_heading("Missing values", "Null-value count for each source column.")
        missing = df.isnull().sum().rename_axis("Column").reset_index(name="Missing values")
        st.dataframe(missing, width="stretch", hide_index=True, height=360)
    with right:
        section_heading("Statistical summary", "Summary of numeric and categorical fields.")
        st.dataframe(df.describe(include="all").T, width="stretch", height=360)

elif page == "Project Information":
    show_header("Project Information", "A practical, transparent look at the analysis.")
    left, right = st.columns(2)
    with left:
        st.markdown(
            """
            <div class="project-card">
                <div class="eyebrow">Project objective</div>
                <h3>Turning accident records into actionable context.</h3>
                <p>Explore road-safety patterns across time, location, vehicle type, severity and weather. 
                All dashboard metrics and insights are calculated from the loaded dataset and current filters.</p>
                <h4>Core capabilities</h4>
                <ul>
                    <li>CSV upload and dataset normalization</li>
                    <li>Interactive filters and responsive visualizations</li>
                    <li>Location, severity and casualty analysis</li>
                    <li>Search, missing-value review and CSV export</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="project-card">
                <div class="eyebrow">Technology & methodology</div>
                <h3>Built with a clear and reproducible workflow.</h3>
                <ul>
                    <li><b>Python</b> for data processing</li>
                    <li><b>Streamlit</b> for the interactive application</li>
                    <li><b>Pandas & NumPy</b> for data preparation</li>
                    <li><b>Plotly</b> for interactive visual analysis</li>
                </ul>
                <h4>Interpreting the metrics</h4>
                <p>Accident totals count rows, so each row should represent one accident. Casualties and fatalities are 
                separate measures; fatality totals are shown only when the dataset provides them. Charts are omitted 
                when their required fields are missing or empty.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.caption(f"Current source: {source_name} · {len(df):,} records · {len(df.columns)} columns")
