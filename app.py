import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="India Census Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 12% 0%, rgba(79,70,229,.20), transparent 34%),
        radial-gradient(ellipse at 88% 12%, rgba(6,182,212,.12), transparent 30%),
        linear-gradient(145deg, #030407 0%, #080b13 48%, #05070c 100%);
    color: #edf2ff;
}

.block-container {
    max-width: 1800px;
    padding: 2rem 2rem 1rem;
}

header[data-testid="stHeader"] {
    background: rgba(3,4,7,.55);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090d17 0%, #05070c 100%);
    border-right: 1px solid rgba(129,140,248,.22);
}

section[data-testid="stSidebar"] * {
    color: #edf2ff;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(148,163,184,.20);
}

.sidebar-brand {
    text-align: center;
    padding: 12px 0 20px;
}

.sidebar-brand .flag {
    font-size: 44px;
    filter: drop-shadow(0 0 12px rgba(99,102,241,.45));
}

.sidebar-brand .name {
    font-size: 24px;
    font-weight: 850;
    color: #fff;
}

.sidebar-brand .caption {
    font-size: 11px;
    color: #a5b4fc;
    letter-spacing: 2px;
    margin-top: 5px;
}

.sidebar-section {
    color: #a5b4fc !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin: 15px 0 10px;
}

.dashboard-title {
    text-align: center;
    font-size: clamp(27px, 3vw, 42px);
    font-weight: 900;
    letter-spacing: -1.1px;
    color: #fff;
    margin: 0;
    text-shadow: 0 0 28px rgba(99,102,241,.25);
}

.dashboard-subtitle {
    text-align: center;
    color: #aab6ce;
    font-size: 14px;
    margin: 10px 0 28px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(23,29,47,.96), rgba(9,13,23,.96)) !important;
    border: 1px solid rgba(129,140,248,.27) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.035) !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label,
div[data-testid="stMetricLabel"] span {
    color: #b7c3da !important;
    opacity: 1 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div,
div[data-testid="stMetricValue"] label {
    color: #fff !important;
    opacity: 1 !important;
    font-size: clamp(22px, 2vw, 30px) !important;
    font-weight: 850 !important;
}

div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] svg {
    color: #67e8f9 !important;
    fill: #67e8f9 !important;
}

.section-heading {
    color: #f5f7ff;
    font-size: 22px;
    font-weight: 850;
    margin-top: 22px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #9aa9c3;
    font-size: 13px;
    margin-bottom: 18px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #111827;
    border: 1px solid #36415a;
    border-radius: 9px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #fff;
}

section[data-testid="stSidebar"] input {
    color: #fff !important;
}

.stButton > button {
    width: 100%;
    min-height: 44px;
    border: 1px solid rgba(165,180,252,.35);
    border-radius: 10px;
    background: linear-gradient(100deg, #4f46e5, #2563eb 58%, #0891b2);
    color: #fff;
    font-weight: 800;
    transition: all .2s ease;
    box-shadow: 0 5px 22px rgba(79,70,229,.20);
}

.stButton > button:hover {
    background: linear-gradient(100deg, #6366f1, #3b82f6, #06b6d4);
    border-color: #67e8f9;
    box-shadow: 0 0 22px rgba(34,211,238,.20);
}

div[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(15,20,34,.92), rgba(5,7,12,.95));
    border: 1px solid rgba(129,140,248,.22);
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 8px 30px rgba(0,0,0,.28);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
    background: rgba(17,24,39,.82);
}

.state-summary {
    background: linear-gradient(135deg, rgba(20,27,47,.97), rgba(8,12,22,.97));
    border: 1px solid rgba(103,232,249,.26);
    border-radius: 18px;
    padding: 20px 22px;
    margin: 12px 0 24px;
    box-shadow: 0 10px 32px rgba(0,0,0,.28), 0 0 24px rgba(79,70,229,.08);
}

.state-summary-title {
    color: #67e8f9;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.6px;
    text-transform: uppercase;
}

.state-summary-name {
    color: #fff;
    font-size: 25px;
    font-weight: 900;
    margin: 4px 0 6px;
}

.state-summary-copy {
    color: #aab6ce;
    font-size: 13px;
}

.dashboard-footer {
    text-align: center;
    color: #71809a;
    font-size: 11px;
    padding: 20px 0;
    letter-spacing: .5px;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .dashboard-title {
        font-size: 27px;
    }

    div[data-testid="stMetric"] {
        padding: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_csv("india.csv")
    data.columns = data.columns.str.strip()

    for col in ["Latitude", "Longitude"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


try:
    df = load_data()
except FileNotFoundError:
    st.error("india.csv was not found. Keep it in the same directory as app.py.")
    st.stop()


required_columns = ["Latitude", "Longitude", "State", "District"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()


with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="flag">🇮🇳</div>
        <div class="name">Census Explorer</div>
        <div class="caption">INDIA · 2011</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<div class="sidebar-section">01 / GEOGRAPHIC SELECTION</div>',
        unsafe_allow_html=True
    )

    states = sorted(df["State"].dropna().unique().tolist())
    state_options = ["Overall India"] + states

    selected_state = st.selectbox("Select State", state_options)

    st.divider()

    st.markdown(
        '<div class="sidebar-section">02 / VISUALIZATION SETTINGS</div>',
        unsafe_allow_html=True
    )

    parameters = df.columns[6:].tolist()

    if not parameters:
        st.error("No visualization parameters were found.")
        st.stop()

    primary = st.selectbox(
        "Primary Parameter · Marker Size",
        parameters
    )

    secondary = st.selectbox(
        "Secondary Parameter · Marker Color",
        parameters,
        index=min(1, len(parameters) - 1)
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">03 / GENERATE MAP</div>',
        unsafe_allow_html=True
    )

    plot = st.button(
        "✦ Generate Census Map",
        use_container_width=True
    )


# Dynamic page heading
page_title = (
    "🇮🇳 India Census Dashboard"
    if selected_state == "Overall India"
    else selected_state
)

page_subtitle = (
    "Explore India's demographic landscape through interactive visualization."
    if selected_state == "Overall India"
    else f"District-level demographic profile and geographic insights for {selected_state} · Census 2011"
)

st.markdown(
    f"""
    <div class="dashboard-title">{page_title}</div><div class="dashboard-subtitle">{page_subtitle}</div>
    """,
    unsafe_allow_html=True
)


# Selected geographic scope
scope_df = (
    df.copy()
    if selected_state == "Overall India"
    else df[df["State"] == selected_state].copy()
)

total_states = scope_df["State"].nunique()
total_districts = scope_df["District"].nunique()


def find_column(frame, candidates):
    columns = {
        str(column).strip().lower(): column
        for column in frame.columns
    }

    for candidate in candidates:
        key = candidate.strip().lower()
        if key in columns:
            return columns[key]

    return None


def sum_numeric_column(frame, column):
    if column is None:
        return None

    values = pd.to_numeric(frame[column], errors="coerce")
    total = values.sum(min_count=1)

    return total if pd.notna(total) else None


def format_count(value):
    if value is not None and pd.notna(value):
        return f"{value:,.0f}"

    return "N/A"


population_col = find_column(
    scope_df,
    ["Population", "Total Population", "TOT_P", "Total population"]
)

population_total = sum_numeric_column(scope_df, population_col)
population_display = format_count(population_total)


# State demographic panel
if selected_state != "Overall India":

    male_col = find_column(
        scope_df,
        ["Male Population", "Male", "Males", "TOT_M", "Total Male"]
    )

    female_col = find_column(
        scope_df,
        ["Female Population", "Female", "Females", "TOT_F", "Total Female"]
    )

    sex_ratio_col = find_column(
        scope_df,
        ["Sex Ratio", "Sex_Ratio", "Sex ratio"]
    )

    literacy_col = find_column(
        scope_df,
        ["Literacy Rate", "Literacy", "Literacy_Rate", "Literacy rate"]
    )

    male_population = sum_numeric_column(scope_df, male_col)
    female_population = sum_numeric_column(scope_df, female_col)

    if sex_ratio_col:
        sex_ratios = pd.to_numeric(
            scope_df[sex_ratio_col],
            errors="coerce"
        ).dropna()

        sex_ratio_display = (
            f"{sex_ratios.mean():,.1f}"
            if not sex_ratios.empty
            else "N/A"
        )

    elif (
        male_population is not None
        and male_population > 0
        and female_population is not None
    ):
        sex_ratio_display = f"{female_population / male_population * 1000:,.1f}"

    else:
        sex_ratio_display = "N/A"

    if literacy_col:
        literacy_values = pd.to_numeric(
            scope_df[literacy_col],
            errors="coerce"
        ).dropna()

        literacy_display = (
            f"{literacy_values.mean():,.2f}%"
            if not literacy_values.empty
            else "N/A"
        )
    else:
        literacy_display = "N/A"

    state_district_count = scope_df["District"].nunique()

    # IMPORTANT: Keep the HTML tags contiguous and enable HTML rendering.
    # This prevents the remaining tags from appearing as visible code.
    state_summary_html = (
        '<div class="state-summary">'
        '<div class="state-summary-title">SELECTED STATE · CENSUS 2011</div>'
        f'<div class="state-summary-name">{selected_state}</div>'
        '<div class="state-summary-copy">'
        'Demographic overview aggregated from the available district records in your CSV.'
        '</div>'
        '</div>'
    )

    st.markdown(
        state_summary_html,
        unsafe_allow_html=True
    )

    state_metric_columns = st.columns(6)

    state_metrics = [
        ("Total Population", format_count(population_total)),
        ("Male Population", format_count(male_population)),
        ("Female Population", format_count(female_population)),
        ("Sex Ratio (♀ per 1,000 ♂)", sex_ratio_display),
        ("Literacy Rate", literacy_display),
        ("Districts", f"{state_district_count:,}")
    ]

    for metric_column, (metric_label, metric_value) in zip(
        state_metric_columns,
        state_metrics
    ):
        with metric_column:
            st.metric(metric_label, metric_value)


# Main statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("States / UTs Represented", f"{total_states:,}")

with col2:
    st.metric("Districts Represented", f"{total_districts:,}")

with col3:
    st.metric("Population Total", population_display)


st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-heading">Geographic Intelligence</div><div class="section-subtitle">Explore regional patterns and inspect district data on the map.</div>
""", unsafe_allow_html=True)


# Preserve the original map-generation workflow
if "map_generated" not in st.session_state:
    st.session_state.map_generated = False

if plot:
    st.session_state.map_generated = True


if not st.session_state.map_generated:

    st.info(
        "Select your region and parameters from the sidebar, "
        "then click Generate Census Map."
    )

else:

    if selected_state == "Overall India":
        map_df = df.copy()
        center_lat = 22.5937
        center_lon = 78.9629
        zoom_level = 3.8

    else:
        map_df = df[df["State"] == selected_state].copy()

        if map_df.empty:
            st.warning("No records found for the selected state.")
            st.stop()

        center_lat = map_df["Latitude"].mean()
        center_lon = map_df["Longitude"].mean()
        zoom_level = 5

    map_df[primary] = pd.to_numeric(
        map_df[primary],
        errors="coerce"
    )

    map_df.loc[map_df[primary] <= 0, primary] = np.nan

    map_df[secondary] = map_df[secondary].replace(
        r"^\s*$",
        np.nan,
        regex=True
    )

    map_df = map_df.dropna(
        subset=[
            "Latitude",
            "Longitude",
            primary,
            secondary,
            "District"
        ]
    )

    if map_df.empty:
        st.warning(
            "No valid data for the selected parameters. "
            "Try another primary or secondary parameter."
        )
        st.stop()

    numeric_secondary = pd.to_numeric(
        map_df[secondary],
        errors="coerce"
    )

    if pd.api.types.is_numeric_dtype(map_df[secondary]):
        color_mode = "continuous"

    elif numeric_secondary.notna().all():
        map_df[secondary] = numeric_secondary
        color_mode = "continuous"

    else:
        color_mode = "categorical"

    map_args = {
        "data_frame": map_df,
        "lat": "Latitude",
        "lon": "Longitude",
        "color": secondary,
        "size": primary,
        "text": "District",
        "zoom": zoom_level,
        "center": {
            "lat": center_lat,
            "lon": center_lon
        },
        "map_style": "carto-darkmatter",
        "hover_name": "District",
        "height": 720,
        "size_max": 32
    }

    if color_mode == "continuous":
        map_args["color_continuous_scale"] = "Viridis"
    else:
        map_args["color_discrete_sequence"] = px.colors.qualitative.Bold

    fig = px.scatter_map(**map_args)

    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=15, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial, sans-serif",
            color="#e5edff",
            size=12
        ),
        legend_title_text=secondary
    )

    # Compatible with Plotly Scattermap markers.
    # Do not use marker.line here.
    fig.update_traces(
        marker=dict(opacity=0.88),
        textposition="top center",
        textfont=dict(
            size=9,
            color="#f8fafc"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "responsive": True,
            "displaylogo": False,
            "scrollZoom": True
        }
    )

    st.caption(
        f"Region: {selected_state} · "
        f"Records displayed: {len(map_df):,} · "
        f"Marker size: {primary} · "
        f"Marker color: {secondary}"
    )


st.divider()

st.markdown("""
<div class="dashboard-footer">INDIA CENSUS EXPLORER · 2011<br>Built with Streamlit and Plotly</div>
""", unsafe_allow_html=True)