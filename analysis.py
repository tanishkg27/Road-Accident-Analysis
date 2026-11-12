import pandas as pd
import plotly.express as px

BURGUNDY = "#702C3B"
DEEP_BURGUNDY = "#4A1F2B"
SAGE_GREY = "#A3A99B"
CREAM_BEIGE = "#F3EBDD"
SOFT_WHITE = "#FAF8F3"
MUTED_GREY = "#77796F"
CHART_COLORS = [BURGUNDY, SAGE_GREY, DEEP_BURGUNDY, "#C6A7A0", "#D8C8AE"]
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
DAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]


def _ordered_counts(df, column):
    if column not in df.columns:
        return None
    data = df[column].dropna().astype(str).value_counts().rename_axis(column).reset_index(name="count")
    if data.empty:
        return None

    if column == "year":
        data["_sort"] = pd.to_numeric(data[column], errors="coerce")
        data = data.sort_values("_sort", kind="stable", na_position="last").drop(columns="_sort")
    elif column == "month":
        month_ranks = {month.lower(): index for index, month in enumerate(MONTH_ORDER)}
        data["_sort"] = data[column].str.lower().map(month_ranks)
        data = data.sort_values("_sort", kind="stable", na_position="last").drop(columns="_sort")
    elif column == "day":
        day_ranks = {day.lower(): index for index, day in enumerate(DAY_ORDER)}
        data["_sort"] = data[column].str.lower().map(day_ranks)
        data = data.sort_values("_sort", kind="stable", na_position="last").drop(columns="_sort")
    return data


def _style_figure(fig, title):
    fig.update_layout(
        title=dict(text=title, x=0.02, xanchor="left", font=dict(size=17, color=DEEP_BURGUNDY)),
        template="plotly_white",
        paper_bgcolor=SOFT_WHITE,
        plot_bgcolor=CREAM_BEIGE,
        font=dict(family="Arial, sans-serif", color=MUTED_GREY, size=12),
        margin=dict(l=18, r=18, t=58, b=24),
        hoverlabel=dict(bgcolor=DEEP_BURGUNDY, font_color=SOFT_WHITE, bordercolor=DEEP_BURGUNDY),
        legend=dict(
            bgcolor="rgba(250,248,243,0)",
            font=dict(color=MUTED_GREY),
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=CREAM_BEIGE)
    fig.update_yaxes(showgrid=True, gridcolor="#EAE5DC", zeroline=False, linecolor=CREAM_BEIGE)
    return fig


def create_bar_chart(df, column, title):
    data = _ordered_counts(df, column)
    if data is None:
        return None
    fig = px.bar(
        data, x=column, y="count", color_discrete_sequence=[BURGUNDY],
        labels={column: "", "count": "Accidents"},
        hover_data={"count": ":,d"},
    )
    fig.update_traces(marker_line_width=0, hovertemplate="%{x}<br>Accidents: %{y:,}<extra></extra>")
    fig.update_layout(hovermode="x unified", showlegend=False)
    return _style_figure(fig, title)


def create_pie_chart(df, column, title):
    data = _ordered_counts(df, column)
    if data is None:
        return None
    fig = px.pie(
        data, names=column, values="count", hole=0.62,
        color_discrete_sequence=CHART_COLORS,
        hover_data={"count": ":,d"},
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        marker=dict(line=dict(color=SOFT_WHITE, width=3)),
        hovertemplate="%{label}<br>Accidents: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    return _style_figure(fig, title)


def create_line_chart(df, column, title):
    data = _ordered_counts(df, column)
    if data is None:
        return None
    fig = px.line(
        data, x=column, y="count", markers=True,
        color_discrete_sequence=[BURGUNDY],
        labels={column: "", "count": "Accidents"},
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8, color=BURGUNDY, line=dict(color=SOFT_WHITE, width=2)),
        hovertemplate="%{x}<br>Accidents: %{y:,}<extra></extra>",
    )
    fig.update_layout(hovermode="x unified", showlegend=False)
    return _style_figure(fig, title)


def create_top_locations_chart(df, limit=10):
    data = _ordered_counts(df, "location")
    if data is None:
        return None
    data = data.nlargest(limit, "count").sort_values("count", ascending=True)
    fig = px.bar(
        data, x="count", y="location", orientation="h",
        color_discrete_sequence=[BURGUNDY],
        labels={"location": "", "count": "Accidents"},
        hover_data={"count": ":,d"},
    )
    fig.update_traces(marker_line_width=0, hovertemplate="%{y}<br>Accidents: %{x:,}<extra></extra>")
    fig.update_layout(showlegend=False, yaxis=dict(showgrid=False))
    return _style_figure(fig, "Top 10 Accident-Prone Locations")


def create_casualties_chart(df):
    available = [column for column in ("casualties", "fatalities") if column in df.columns]
    if not available:
        return None
    totals = [pd.to_numeric(df[column], errors="coerce").sum(min_count=1) for column in available]
    data = pd.DataFrame({"Measure": available, "Total": totals}).dropna(subset=["Total"])
    if data.empty:
        return None
    labels = {"casualties": "Casualties", "fatalities": "Fatalities"}
    data["Measure"] = data["Measure"].map(labels)
    fig = px.bar(
        data, x="Measure", y="Total", color="Measure",
        color_discrete_map={"Casualties": SAGE_GREY, "Fatalities": BURGUNDY},
        labels={"Measure": "", "Total": "People"},
        text_auto=".0f",
    )
    fig.update_traces(marker_line_width=0, hovertemplate="%{x}<br>People: %{y:,.0f}<extra></extra>")
    fig.update_layout(showlegend=False)
    return _style_figure(fig, "Casualties vs Fatalities")


def get_top_location(df):
    if "location" not in df.columns:
        return "Not Available"
    locations = df["location"].dropna().astype(str)
    if locations.empty:
        return "Not Available"
    return str(locations.value_counts().idxmax())


def get_insights(df):
    insights = []
    if df.empty:
        return insights

    if "year" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce").dropna()
        if not years.empty:
            year_counts = years.value_counts()
            insights.append(
                f"Highest accident count: {int(year_counts.max()):,} in {int(year_counts.idxmax())}."
            )

    location = get_top_location(df)
    if location != "Not Available":
        insights.append(f"Most accident-prone location: {location}.")

    if "vehicle" in df.columns:
        vehicles = df["vehicle"].dropna().astype(str)
        if not vehicles.empty:
            insights.append(f"Most frequently involved vehicle: {vehicles.value_counts().idxmax()}.")

    if "time" in df.columns:
        times = pd.to_datetime(df["time"].astype(str), format="%H:%M", errors="coerce")
        hours = times.dropna().dt.hour
        if not hours.empty:
            insights.append(f"Most common accident time: {int(hours.value_counts().idxmax()):02d}:00.")

    if "severity" in df.columns:
        severities = df["severity"].dropna().astype(str)
        if not severities.empty:
            insights.append(f"Most common accident severity: {severities.value_counts().idxmax()}.")

    return insights
