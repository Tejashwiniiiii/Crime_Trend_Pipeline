
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URL

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Crime Trend Analytics",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

[data-testid="stSidebar"] {
    background-color: #101D35;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #142B4A;
    margin-bottom: 4px;
}

.subtitle {
    color: #64748B;
    font-size: 15px;
    margin-bottom: 25px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

.metric-label {
    color: #64748B;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #142B4A;
    font-size: 29px;
    font-weight: 800;
    margin-top: 7px;
}

.section-title {
    color: #142B4A;
    font-size: 21px;
    font-weight: 750;
    margin-top: 15px;
}

div[data-testid="stDownloadButton"] button {
    background-color: #173B67;
    color: white;
    border-radius: 8px;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DATABASE CONNECTION
# ==========================================

@st.cache_resource
def get_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(ttl=60)
def load_data():

    engine = get_engine()

    with engine.connect() as connection:

        df = pd.read_sql(
            text("SELECT * FROM crime_data"),
            connection
        )

    if df.empty:
        return df

    df["date_time"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    df = df.dropna(subset=["date_time"]).copy()

    # Create analysis columns if not already available
    if "year" not in df.columns:
        df["year"] = df["date_time"].dt.year

    if "month" not in df.columns:
        df["month"] = df["date_time"].dt.month

    if "hour" not in df.columns:
        df["hour"] = df["date_time"].dt.hour

    if "day_name" not in df.columns:
        df["day_name"] = df["date_time"].dt.day_name()

    if "time_period" not in df.columns:

        hour = df["date_time"].dt.hour

        df["time_period"] = hour.apply(
            lambda x:
            "Morning" if 5 <= x <= 11 else
            "Afternoon" if 12 <= x <= 16 else
            "Evening" if 17 <= x <= 20 else
            "Night"
        )

    for column in ["type", "subtype", "location"]:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("Not Available")
                .astype(str)
            )

    return df


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🚨 Crime Trend Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Cambridge Police Department | Local Crime Monitoring & Analysis'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# LOAD DATABASE
# ==========================================

try:

    df = load_data()

    if df.empty:
        st.warning("No crime records are currently available.")
        st.stop()

    st.success(
        f"Database connected successfully | "
        f"{len(df):,} records available"
    )

    # ======================================
    # SIDEBAR FILTERS
    # ======================================

    st.sidebar.title("🚨 Crime Analytics")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Dashboard Filters")

    crime_types = sorted(
        df["type"].dropna().unique().tolist()
    )

    selected_types = st.sidebar.multiselect(
        "Crime Type",
        crime_types,
        default=crime_types
    )

    years = sorted(
        df["year"].dropna().unique().tolist(),
        reverse=True
    )

    selected_years = st.sidebar.multiselect(
        "Select Year",
        years,
        default=years
    )

    periods = [
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ]

    selected_periods = st.sidebar.multiselect(
        "Time Period",
        periods,
        default=periods
    )

    # Date range filter
    min_date = df["date_time"].min().date()
    max_date = df["date_time"].max().date()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("🔄 Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.caption(
        "Data Source: Cambridge Police Open Data"
    )

    # ======================================
    # APPLY FILTERS
    # ======================================

    filtered_df = df[
        (df["type"].isin(selected_types)) &
        (df["year"].isin(selected_years)) &
        (df["time_period"].isin(selected_periods))
    ].copy()

    if len(selected_dates) == 2:

        start_date, end_date = selected_dates

        filtered_df = filtered_df[
            (filtered_df["date_time"].dt.date >= start_date) &
            (filtered_df["date_time"].dt.date <= end_date)
        ]

    # ======================================
    # KPI CARDS
    # ======================================

    st.markdown(
        '<div class="section-title">📊 Crime Overview</div>',
        unsafe_allow_html=True
    )

    total_records = len(filtered_df)

    total_types = filtered_df["type"].nunique()

    total_locations = (
        filtered_df["location"].nunique()
        if "location" in filtered_df.columns else 0
    )

    total_years = filtered_df["year"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "TOTAL CRIME RECORDS", f"{total_records:,}"),
        (col2, "CRIME CATEGORIES", f"{total_types:,}"),
        (col3, "LOCATIONS", f"{total_locations:,}"),
        (col4, "YEARS COVERED", f"{total_years:,}")
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    if filtered_df.empty:
        st.warning(
            "No records match the selected filters. "
            "Please change your filters."
        )
        st.stop()

    # ======================================
    # CRIME TYPE ANALYSIS
    # ======================================

    st.markdown(
        '<div class="section-title">📌 Crime Distribution Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Crime Distribution by Type")

        crime_counts = (
            filtered_df["type"]
            .value_counts()
            .reset_index()
        )

        crime_counts.columns = ["Crime Type", "Count"]

        st.bar_chart(
            crime_counts,
            x="Crime Type",
            y="Count",
            color="#2563EB"
        )

    with col2:

        st.subheader("Crime Distribution by Time Period")

        period_counts = (
            filtered_df["time_period"]
            .value_counts()
            .reindex(periods, fill_value=0)
        )

        st.bar_chart(
            period_counts,
            color="#0D9488"
        )

    # ======================================
    # MONTHLY TREND ANALYSIS
    # ======================================

    st.markdown(
        '<div class="section-title">📈 Crime Trend Analysis</div>',
        unsafe_allow_html=True
    )

    monthly_data = filtered_df.copy()

    monthly_data["Month"] = (
        monthly_data["date_time"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_counts = (
        monthly_data.groupby("Month")
        .size()
        .reset_index(name="Crime Records")
        .sort_values("Month")
    )

    st.subheader("Monthly Crime Trends")

    st.line_chart(
        monthly_counts,
        x="Month",
        y="Crime Records",
        color="#2563EB"
    )

    # ======================================
    # DAY AND HOUR ANALYSIS
    # ======================================

    st.markdown(
        '<div class="section-title">🕒 Time-Based Crime Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    with col1:

        st.subheader("Crime Records by Day")

        day_counts = (
            filtered_df["day_name"]
            .value_counts()
            .reindex(day_order, fill_value=0)
        )

        st.bar_chart(
            day_counts,
            color="#7C3AED"
        )

    with col2:

        st.subheader("Crime Records by Hour")

        hourly_counts = (
            filtered_df["hour"]
            .value_counts()
            .reindex(range(24), fill_value=0)
            .sort_index()
        )

        st.line_chart(
            hourly_counts,
            color="#EA580C"
        )

    # ======================================
    # LOCATION ANALYSIS
    # ======================================

    st.markdown(
        '<div class="section-title">📍 Location Analysis</div>',
        unsafe_allow_html=True
    )

    if "location" in filtered_df.columns:

        location_counts = (
            filtered_df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        location_counts.columns = [
            "Location",
            "Crime Records"
        ]

        st.subheader("Top 10 Crime Locations")

        st.bar_chart(
            location_counts,
            x="Location",
            y="Crime Records",
            color="#DC2626"
        )

    # ======================================
    # DETAILED CRIME RECORDS
    # ======================================

    st.markdown(
        '<div class="section-title">📋 Detailed Crime Records</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "🔍 Search crime records",
        placeholder="Search by crime type, location, description..."
    )

    display_df = filtered_df.copy()

    if search.strip():

        searchable_columns = [
            column for column in [
                "type",
                "subtype",
                "location",
                "description"
            ]
            if column in display_df.columns
        ]

        mask = display_df[
            searchable_columns
        ].astype(str).apply(
            lambda column: column.str.contains(
                search,
                case=False,
                na=False,
                regex=False
            )
        ).any(axis=1)

        display_df = display_df[mask]

    st.caption(
        f"Showing {len(display_df):,} matching records"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # DOWNLOAD DATA
    # ======================================

    st.markdown("---")

    st.subheader("📥 Export Crime Data")

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇ Download Filtered Crime Data",
        data=csv_data,
        file_name="cambridge_crime_analysis.csv",
        mime="text/csv"
    )

    st.caption(
        "Local Crime Trend Monitoring Dashboard | "
        "Data analysis using Python, Streamlit and PostgreSQL"
    )

except Exception as error:

    st.error("Unable to load the crime dashboard.")

    st.exception(error)
