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
    background: #f4f7fb;
    color: #172033;
}

.block-container {
    max-width: 1800px;
    padding: 2rem 2rem 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263247;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

section[data-testid="stSidebar"] hr {
    border-color: #374151;
}

.sidebar-brand {
    text-align: center;
    padding: 12px 0 20px;
}

.sidebar-brand .flag {
    font-size: 44px;
}

.sidebar-brand .name {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
}

.sidebar-brand .caption {
    font-size: 12px;
    color: #a5b4fc;
    letter-spacing: 2px;
    margin-top: 5px;
}

.sidebar-section {
    color: #a5b4fc !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin: 15px 0 10px;
}

/* Main heading */
.dashboard-title {
    text-align: center;
    font-size: clamp(27px, 3vw, 42px);
    font-weight: 850;
    letter-spacing: -1.2px;
    color: #111827;
    margin: 0;
}

.dashboard-subtitle {
    text-align: center;
    color: #526179;
    font-size: 15px;
    margin: 10px 0 30px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
    padding: 22px !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15) !important;
}

/* Metric labels */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label,
div[data-testid="stMetricLabel"] span {
    color: #e2e8f0 !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

/* Metric values */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div,
div[data-testid="stMetricValue"] label {
    color: #ffffff !important;
    opacity: 1 !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* Metric delta */
div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] svg {
    color: #a5b4fc !important;
    fill: #a5b4fc !important;
}

/* Section headings */
.section-heading {
    color: #111827;
    font-size: 23px;
    font-weight: 800;
    margin-top: 22px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #526179;
    font-size: 14px;
    margin-bottom: 18px;
}

/* Sidebar inputs */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #202b3c;
    border: 1px solid #455168;
    border-radius: 9px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #ffffff;
}

section[data-testid="stSidebar"] input {
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 44px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(100deg, #4f46e5, #6366f1);
    color: #ffffff;
    font-weight: 750;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(100deg, #4338ca, #4f46e5);
    border: none;
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.25);
}

/* Map */
div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #dbe3ef;
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.05);
}

/* Messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */
.dashboard-footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 20px 0;
}

/* Responsive design */
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

    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
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

    st.markdown("""
    <div style="
        margin-top:28px;
        padding:15px;
        background:#1f2937;
        border:1px solid #374151;
        border-radius:12px;
    ">
        <div style="color:#a5b4fc;font-size:11px;font-weight:800;">
            DATA SOURCE
        </div>
        <div style="color:#ffffff;font-size:14px;margin-top:8px;">
            Indian Census 2011
        </div>
        <div style="color:#cbd5e1;font-size:12px;margin-top:5px;">
            Geographic and demographic analysis
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="dashboard-title">🇮🇳 India Census Dashboard</div>
<div class="dashboard-subtitle">
    Explore India's demographic landscape through interactive visualization.
</div>
""", unsafe_allow_html=True)


total_states = df["State"].nunique()
total_districts = df["District"].nunique()

if "Population" in df.columns:
    population = pd.to_numeric(df["Population"], errors="coerce")
    population_total = population.sum(min_count=1)

    population_display = (
        f"{population_total:,.0f}"
        if pd.notna(population_total)
        else "N/A"
    )
else:
    population_display = "N/A"


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("States / UTs Represented", f"{total_states:,}")

with col2:
    st.metric("Districts Represented", f"{total_districts:,}")

with col3:
    st.metric("Population Total", population_display)


st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-heading">Geographic Intelligence</div>
<div class="section-subtitle">
    Explore regional patterns and hover over markers to inspect district data.
</div>
""", unsafe_allow_html=True)


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

    map_df[primary] = pd.to_numeric(map_df[primary], errors="coerce")
    map_df.loc[map_df[primary] <= 0, primary] = np.nan

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
            "Try another primary parameter."
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
        "zoom": zoom_level,
        "center": {
            "lat": center_lat,
            "lon": center_lon
        },
        "map_style": "carto-positron",
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
        paper_bgcolor="#ffffff",
        font=dict(
            family="Arial, sans-serif",
            color="#334155",
            size=12
        ),
        legend_title_text=secondary
    )

    fig.update_traces(marker=dict(opacity=0.85))

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
        f"Marker size: {primary} · Marker color: {secondary}"
    )


st.divider()

st.markdown("""
<div class="dashboard-footer">
    INDIA CENSUS EXPLORER · 2011<br>
    Built with Streamlit and Plotly
</div>
""", unsafe_allow_html=True)