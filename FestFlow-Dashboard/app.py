import random
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FestFlow | CHRIST University Real-Time Event Hub",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #3B0764 50%, #831843 100%);
        padding: 1.6rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 75, 145, 0.35);
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #FFD166, #FF4B91, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: #E2E8F0;
        font-size: 1rem;
        margin-top: 0.35rem;
    }
    .event-card {
        background: #141B2D;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.9rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .event-card:hover {
        border-color: #FF4B91;
    }
    .badge-live {
        background: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid #EF4444;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .badge-soon {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid #F59E0B;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .badge-upcoming {
        background: rgba(56, 189, 248, 0.18);
        color: #38BDF8;
        border: 1px solid #0EA5E9;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .badge-done {
        background: rgba(34, 197, 94, 0.18);
        color: #4ADE80;
        border: 1px solid #22C55E;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .pass-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 2px dashed #00E5FF;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# INITIAL DATASET (CHRIST UNIVERSITY CENTRAL CAMPUS FESTS & VENUES)
# -----------------------------------------------------------------------------
IST = timezone(timedelta(hours=5, minutes=30))


def get_initial_events():
    return pd.DataFrame(
        [
            {
                "id": "EVT-101",
                "name": "Gateways AI Hackathon",
                "fest": "Gateways (MCA)",
                "category": "Tech",
                "icon": "💻",
                "venue": "Skyview (Block 4)",
                "x": 6.5,
                "y": 7.8,
                "start_hour": 9.5,
                "end_hour": 13.5,
                "capacity": 240,
                "crowd": 212,
                "vibe_score": 94,
                "noise_db": 74,
                "organizer": "Dept. of Computer Science",
                "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-102",
                "name": "Nritya Sangam: Classical Solo",
                "fest": "Blossoms",
                "category": "Dance",
                "icon": "💃",
                "venue": "Main Auditorium",
                "x": 2.2,
                "y": 5.0,
                "start_hour": 10.0,
                "end_hour": 12.5,
                "capacity": 1200,
                "crowd": 1090,
                "vibe_score": 97,
                "noise_db": 86,
                "organizer": "SWO Cultural Wing",
                "image": "https://images.unsplash.com/photo-1545959570-a94084071b5d?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-103",
                "name": "NextWave AI Tech Summit",
                "fest": "NextWave",
                "category": "Tech",
                "icon": "🤖",
                "venue": "KE Auditorium",
                "x": 8.2,
                "y": 4.2,
                "start_hour": 11.0,
                "end_hour": 14.0,
                "capacity": 650,
                "crowd": 540,
                "vibe_score": 91,
                "noise_db": 71,
                "organizer": "Centre for AI",
                "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-104",
                "name": "Battle of the Bands",
                "fest": "In-Bloom",
                "category": "Music",
                "icon": "🎸",
                "venue": "Birds Park Open Stage",
                "x": 4.8,
                "y": 2.4,
                "start_hour": 13.0,
                "end_hour": 16.5,
                "capacity": 900,
                "crowd": 760,
                "vibe_score": 96,
                "noise_db": 95,
                "organizer": "Choir & Music Club",
                "image": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-105",
                "name": "Valorant & FIFA Arena",
                "fest": "Gateways (MCA)",
                "category": "Gaming",
                "icon": "🎮",
                "venue": "Block 2 Seminar Hall",
                "x": 5.5,
                "y": 6.2,
                "start_hour": 12.0,
                "end_hour": 15.5,
                "capacity": 180,
                "crowd": 168,
                "vibe_score": 93,
                "noise_db": 84,
                "organizer": "MCA Gaming Guild",
                "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-106",
                "name": "Curtains Up: Street Theatre",
                "fest": "Darpan",
                "category": "Theatre",
                "icon": "🎭",
                "venue": "Campus View Auditorium",
                "x": 3.4,
                "y": 8.0,
                "start_hour": 14.0,
                "end_hour": 17.0,
                "capacity": 500,
                "crowd": 320,
                "vibe_score": 88,
                "noise_db": 79,
                "organizer": "Dept. of Theatre Studies",
                "image": "https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-107",
                "name": "FinTech Shark Tank Pitch",
                "fest": "Eklavya",
                "category": "Business",
                "icon": "📊",
                "venue": "MBA Block Auditorium",
                "x": 7.4,
                "y": 2.0,
                "start_hour": 15.0,
                "end_hour": 17.5,
                "capacity": 350,
                "crowd": 215,
                "vibe_score": 85,
                "noise_db": 68,
                "organizer": "School of Business",
                "image": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80",
            },
            {
                "id": "EVT-108",
                "name": "Starlight Pro-Show & DJ Night",
                "fest": "In-Bloom",
                "category": "Music",
                "icon": "🎆",
                "venue": "Central Block Plaza",
                "x": 4.2,
                "y": 4.8,
                "start_hour": 17.5,
                "end_hour": 20.5,
                "capacity": 2000,
                "crowd": 1450,
                "vibe_score": 99,
                "noise_db": 98,
                "organizer": "Student Council",
                "image": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=800&q=80",
            },
        ]
    )


def get_initial_leaderboard():
    return pd.DataFrame(
        [
            {"Department": "MCA (Computer Science)", "Points": 485, "Gold": 5, "Silver": 3},
            {"Department": "B.Tech (Kengeri)", "Points": 460, "Gold": 4, "Silver": 4},
            {"Department": "School of Business (MBA)", "Points": 430, "Gold": 4, "Silver": 2},
            {"Department": "Commerce & Finance", "Points": 410, "Gold": 3, "Silver": 5},
            {"Department": "Arts & Humanities", "Points": 395, "Gold": 3, "Silver": 3},
            {"Department": "BCA (Central Campus)", "Points": 380, "Gold": 2, "Silver": 4},
        ]
    )


# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "events_df" not in st.session_state:
    st.session_state.events_df = get_initial_events()
if "leaderboard_df" not in st.session_state:
    st.session_state.leaderboard_df = get_initial_leaderboard()
if "my_schedule" not in st.session_state:
    st.session_state.my_schedule = ["EVT-101", "EVT-104"]
if "buzz_feed" not in st.session_state:
    st.session_state.buzz_feed = [
        "🔴 [LIVE] Gateways AI Hackathon Round 2 mentoring underway at Skyview!",
        "🔥 [CROWD] Main Auditorium crossing 90% capacity for Nritya Sangam Finals.",
        "⚡ [TROPHY] MCA takes the lead in the Rolling Trophy standings (+25 pts).",
    ]
if "tick_count" not in st.session_state:
    st.session_state.tick_count = 0
if "last_pass" not in st.session_state:
    st.session_state.last_pass = None


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def format_hour(h: float) -> str:
    hours = int(h)
    mins = int(round((h - hours) * 60))
    suffix = "AM" if hours < 12 else "PM"
    display_h = hours if 1 <= hours <= 12 else (hours - 12 if hours > 12 else 12)
    return f"{display_h:02d}:{mins:02d} {suffix}"


def get_event_status(start_h: float, end_h: float, current_h: float) -> tuple[str, str]:
    if start_h <= current_h < end_h:
        return "LIVE NOW", "badge-live"
    elif 0 < (start_h - current_h) <= 1.0:
        return "STARTING SOON", "badge-soon"
    elif current_h < start_h:
        return "UPCOMING", "badge-upcoming"
    return "COMPLETED", "badge-done"


def simulate_realtime_tick():
    """Mutates crowd counts, vibe scores, noise levels, and trophy points in real time."""
    df = st.session_state.events_df.copy()
    for idx, row in df.iterrows():
        delta = random.randint(-12, 18)
        new_crowd = int(np.clip(row["crowd"] + delta, 25, row["capacity"]))
        df.at[idx, "crowd"] = new_crowd
        df.at[idx, "vibe_score"] = int(np.clip(row["vibe_score"] + random.randint(-2, 2), 65, 100))
        df.at[idx, "noise_db"] = int(np.clip(row["noise_db"] + random.randint(-3, 3), 55, 102))
    st.session_state.events_df = df

    lb = st.session_state.leaderboard_df.copy()
    lucky_idx = random.randint(0, len(lb) - 1)
    lb.at[lucky_idx, "Points"] += random.choice([5, 10, 15])
    st.session_state.leaderboard_df = lb.sort_values("Points", ascending=False).reset_index(drop=True)

    st.session_state.tick_count += 1
    hot_event = df.sort_values("vibe_score", ascending=False).iloc[0]
    now_str = datetime.now(IST).strftime("%I:%M:%S %p")
    new_alert = (
        f"📡 [{now_str}] {hot_event['icon']} {hot_event['name']} at {hot_event['venue']} "
        f"hit {hot_event['crowd']}/{hot_event['capacity']} attendees (Vibe: {hot_event['vibe_score']}%)"
    )
    st.session_state.buzz_feed.insert(0, new_alert)
    st.session_state.buzz_feed = st.session_state.buzz_feed[:8]


def detect_clashes(selected_ids: list[str], df: pd.DataFrame) -> list[str]:
    sub = df[df["id"].isin(selected_ids)].sort_values("start_hour").reset_index(drop=True)
    clashes = []
    for i in range(len(sub)):
        for j in range(i + 1, len(sub)):
            if sub.loc[i, "end_hour"] > sub.loc[j, "start_hour"]:
                clashes.append(
                    f"⚠️ **{sub.loc[i, 'name']}** ({format_hour(sub.loc[i, 'start_hour'])}–{format_hour(sub.loc[i, 'end_hour'])}) "
                    f"overlaps with **{sub.loc[j, 'name']}** ({format_hour(sub.loc[j, 'start_hour'])}–{format_hour(sub.loc[j, 'end_hour'])})"
                )
    return clashes


# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS (TIME-TRAVEL SIMULATOR & FILTERS)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎪 FestFlow Controls")
    st.caption("CHRIST (Deemed to be University) • Central Campus")

    live_mode = st.toggle("🟢 Real-Time Auto-Stream (3s)", value=True)
    st.divider()

    st.markdown("### 🕒 Time-Based Engine")
    clock_mode = st.radio(
        "Clock Source",
        ["Fest Time Simulator (Demo)", "Live IST System Clock"],
        help="Use the simulator during VIVA to watch events shift between Upcoming, Live, and Completed.",
    )
    if clock_mode == "Fest Time Simulator (Demo)":
        sim_hour = st.slider(
            "Scrub Fest Day Time",
            min_value=9.0,
            max_value=21.0,
            value=13.25,
            step=0.25,
            format="%.2f hr",
        )
        current_fest_hour = sim_hour
    else:
        now_ist = datetime.now(IST)
        current_fest_hour = now_ist.hour + now_ist.minute / 60.0

    st.info(f"**Active Fest Clock:** `{format_hour(current_fest_hour)}`")
    st.divider()

    categories = ["All"] + sorted(st.session_state.events_df["category"].unique().tolist())
    selected_category = st.selectbox("🎯 Filter by Category", categories)
    status_filter = st.multiselect(
        "📌 Filter by Status",
        ["LIVE NOW", "STARTING SOON", "UPCOMING", "COMPLETED"],
        default=["LIVE NOW", "STARTING SOON", "UPCOMING", "COMPLETED"],
    )

    if st.button("🔄 Reset Telemetry Data", width="stretch"):
        st.session_state.events_df = get_initial_events()
        st.session_state.leaderboard_df = get_initial_leaderboard()
        st.session_state.tick_count = 0
        st.rerun()


# -----------------------------------------------------------------------------
# HERO HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🎪 FestFlow: Real-Time Campus Event Dashboard</div>
        <div class="hero-sub">
            Live Crowd Telemetry • 3D Spatial Campus Analytics • Dynamic Time-Based Schedule • CHRIST University Central Campus
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# REAL-TIME STREAMING FRAGMENT (AUTO-UPDATES WITHOUT FULL PAGE RELOAD)
# -----------------------------------------------------------------------------
run_every = 3 if live_mode else None


@st.fragment(run_every=run_every)
def render_live_dashboard():
    if live_mode:
        simulate_realtime_tick()

    df = st.session_state.events_df.copy()
    df["occupancy_pct"] = (df["crowd"] / df["capacity"] * 100).round(1)
    status_data = df.apply(
        lambda r: get_event_status(r["start_hour"], r["end_hour"], current_fest_hour), axis=1
    )
    df["status"] = [s[0] for s in status_data]
    df["badge_class"] = [s[1] for s in status_data]

    # Apply sidebar filters
    filtered = df[df["status"].isin(status_filter)]
    if selected_category != "All":
        filtered = filtered[filtered["category"] == selected_category]

    # Top Real-Time KPI Row
    live_events_df = df[df["status"] == "LIVE NOW"]
    total_crowd = int(df["crowd"].sum())
    avg_vibe = round(df["vibe_score"].mean(), 1)
    crowded_venues = df[df["occupancy_pct"] >= 85]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 Active Campus Footfall", f"{total_crowd:,}", f"+{random.randint(8, 34)} / min")
    k2.metric("🔴 Events Live Now", f"{len(live_events_df)} / {len(df)}", f"Clock: {format_hour(current_fest_hour)}")
    k3.metric("⚡ Campus Vibe Index", f"{avg_vibe} / 100", f"Stream Tick #{st.session_state.tick_count}")
    k4.metric(
        "🚨 High-Congestion Venues",
        f"{len(crowded_venues)}",
        "Above 85% Capacity" if len(crowded_venues) else "All Clear",
        delta_color="inverse",
    )

    # Smart Crowd-Overflow Recommendation Banner
    if not crowded_venues.empty:
        top_crowded = crowded_venues.sort_values("occupancy_pct", ascending=False).iloc[0]
        alt_venues = df[df["occupancy_pct"] < 75].sort_values("vibe_score", ascending=False)
        alt_text = (
            f"Try **{alt_venues.iloc[0]['icon']} {alt_venues.iloc[0]['name']}** at "
            f"**{alt_venues.iloc[0]['venue']}** ({alt_venues.iloc[0]['occupancy_pct']}% full)."
            if not alt_venues.empty
            else "All venues are currently buzzing!"
        )
        st.warning(
            f"⚠️ **Crowd Alert:** {top_crowded['venue']} ({top_crowded['name']}) is at "
            f"**{top_crowded['occupancy_pct']}% capacity**. Smart Suggestion: {alt_text}"
        )

    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🕒 Time-Based Live Schedule",
            "🧊 3D Campus & Analytics",
            "🎟️ Live Check-In & My Planner",
            "🏆 Rolling Trophy & Live Buzz",
        ]
    )

    # -------------------------------------------------------------------------
    # TAB 1: TIME-BASED EVENT LIST WITH IMAGES & SYMBOLS
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader(f"🕒 Dynamic Event Feed — {format_hour(current_fest_hour)}")
        if filtered.empty:
            st.info("No events match your current filters. Adjust the sidebar filters or scrub the Fest Clock.")
        else:
            order_map = {"LIVE NOW": 0, "STARTING SOON": 1, "UPCOMING": 2, "COMPLETED": 3}
            filtered = filtered.assign(_ord=filtered["status"].map(order_map)).sort_values(
                ["_ord", "start_hour"]
            )

            cols = st.columns(2)
            for idx, (_, ev) in enumerate(filtered.iterrows()):
                with cols[idx % 2]:
                    with st.container(border=True):
                        img_col, info_col = st.columns([1, 1.5])
                        with img_col:
                            st.image(ev["image"], width="stretch")
                        with info_col:
                            st.markdown(
                                f"""
                                <span class="{ev['badge_class']}">{ev['status']}</span>
                                <h4 style="margin:6px 0 2px 0;">{ev['icon']} {ev['name']}</h4>
                                <p style="color:#94A3B8;font-size:0.85rem;margin:0;">
                                    🏛️ <b>{ev['venue']}</b> • 🏷️ {ev['fest']}<br>
                                    ⏰ {format_hour(ev['start_hour'])} – {format_hour(ev['end_hour'])}<br>
                                    🔊 {ev['noise_db']} dB • ⚡ Vibe: <b>{ev['vibe_score']}%</b>
                                </p>
                                """,
                                unsafe_allow_html=True,
                            )
                            st.progress(
                                min(int(ev["occupancy_pct"]), 100),
                                text=f"👥 {ev['crowd']}/{ev['capacity']} ({ev['occupancy_pct']}%)",
                            )

        # Interactive Timeline Gantt Chart
        st.markdown("#### 📅 Campus Fest Timeline")
        base_date = datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0)
        tl_df = df.copy()
        tl_df["Start"] = tl_df["start_hour"].apply(lambda h: base_date + timedelta(hours=h))
        tl_df["Finish"] = tl_df["end_hour"].apply(lambda h: base_date + timedelta(hours=h))
        fig_tl = px.timeline(
            tl_df,
            x_start="Start",
            x_end="Finish",
            y="venue",
            color="status",
            text="name",
            color_discrete_map={
                "LIVE NOW": "#EF4444",
                "STARTING SOON": "#F59E0B",
                "UPCOMING": "#38BDF8",
                "COMPLETED": "#22C55E",
            },
            template="plotly_dark",
        )
        now_marker = base_date + timedelta(hours=current_fest_hour)
        fig_tl.add_vline(x=now_marker, line_dash="dash", line_color="#FFD166")
        fig_tl.update_layout(height=340, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_tl, width="stretch")

    # -------------------------------------------------------------------------
    # TAB 2: 3D INTERACTIVE VISUALIZATIONS
    # -------------------------------------------------------------------------
    with tab2:
        c3d_1, c3d_2 = st.columns(2)

        with c3d_1:
            st.markdown("#### 🗺️ 3D Campus Crowd Density Terrain")
            st.caption("Drag to rotate • Peaks show real-time crowd hotspots across CHRIST Central Campus.")

            gx = np.linspace(0, 10, 40)
            gy = np.linspace(0, 10, 40)
            X, Y = np.meshgrid(gx, gy)
            Z = np.zeros_like(X)
            for _, row in df.iterrows():
                Z += row["occupancy_pct"] * np.exp(-((X - row["x"]) ** 2 + (Y - row["y"]) ** 2) / 1.8)

            fig_surface = go.Figure()
            fig_surface.add_trace(
                go.Surface(
                    x=X,
                    y=Y,
                    z=Z,
                    colorscale="Plasma",
                    opacity=0.82,
                    showscale=False,
                    name="Crowd Density",
                )
            )
            fig_surface.add_trace(
                go.Scatter3d(
                    x=df["x"],
                    y=df["y"],
                    z=df["occupancy_pct"] + 15,
                    mode="markers+text",
                    text=df["icon"] + " " + df["venue"],
                    textposition="top center",
                    marker=dict(
                        size=df["crowd"] / 90 + 6,
                        color=df["vibe_score"],
                        colorscale="Turbo",
                        line=dict(color="white", width=1.5),
                    ),
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Occupancy: %{customdata[0]}%<br>"
                        "Crowd: %{customdata[1]}<br>"
                        "Vibe Score: %{customdata[2]}/100<extra></extra>"
                    ),
                    customdata=df[["occupancy_pct", "crowd", "vibe_score"]].values,
                )
            )
            fig_surface.update_layout(
                template="plotly_dark",
                height=500,
                margin=dict(l=0, r=0, t=10, b=0),
                scene=dict(
                    xaxis_title="Campus West → East",
                    yaxis_title="Campus South → North",
                    zaxis_title="Crowd Heat Index",
                    bgcolor="#0B0F19",
                ),
            )
            st.plotly_chart(fig_surface, width="stretch")

        with c3d_2:
            st.markdown("#### 🧊 3D Event Vibe vs. Crowd vs. Acoustic Energy")
            st.caption("Compare every event across 3 live telemetry dimensions simultaneously.")

            fig_3d_scatter = px.scatter_3d(
                df,
                x="occupancy_pct",
                y="noise_db",
                z="vibe_score",
                size="crowd",
                color="category",
                hover_name="name",
                hover_data=["venue", "status", "crowd", "capacity"],
                template="plotly_dark",
                height=500,
            )
            fig_3d_scatter.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                scene=dict(
                    xaxis_title="Capacity Used (%)",
                    yaxis_title="Acoustic Energy (dB)",
                    zaxis_title="Vibe Score (0–100)",
                    bgcolor="#0B0F19",
                ),
            )
            st.plotly_chart(fig_3d_scatter, width="stretch")

    # -------------------------------------------------------------------------
    # TAB 3: LIVE CHECK-IN DESK & PERSONAL SCHEDULE CLASH DETECTOR
    # -------------------------------------------------------------------------
    with tab3:
        col_reg, col_plan = st.columns([1, 1.15])

        with col_reg:
            st.markdown("#### 🎟️ Live Venue Check-In & Digital Pass")
            st.caption("Simulate scanning a student ID at a venue gate — updates 3D maps & KPIs immediately.")
            with st.form("checkin_form"):
                student_name = st.text_input("Student Name", placeholder="e.g., Aarav Sharma")
                reg_no = st.text_input("CHRIST Register No.", placeholder="e.g., 2647101")
                target_event = st.selectbox("Select Event Venue", df["name"].tolist())
                team_size = st.number_input("Group Size Checking In", min_value=1, max_value=20, value=1)
                submitted = st.form_submit_button("✅ Check In Now", width="stretch")

                if submitted:
                    if not student_name.strip() or not reg_no.strip():
                        st.error("Please enter both Student Name and Register Number.")
                    else:
                        idx_match = st.session_state.events_df[
                            st.session_state.events_df["name"] == target_event
                        ].index[0]
                        cap = st.session_state.events_df.at[idx_match, "capacity"]
                        curr = st.session_state.events_df.at[idx_match, "crowd"]
                        st.session_state.events_df.at[idx_match, "crowd"] = min(cap, curr + int(team_size))
                        st.session_state.last_pass = {
                            "name": student_name.strip(),
                            "reg": reg_no.strip(),
                            "event": target_event,
                            "venue": st.session_state.events_df.at[idx_match, "venue"],
                            "pass_id": f"FF-{random.randint(10000, 99999)}",
                            "time": datetime.now(IST).strftime("%I:%M %p IST"),
                        }
                        st.session_state.buzz_feed.insert(
                            0, f"🎟️ [CHECK-IN] {student_name} (+{team_size}) checked into {target_event}!"
                        )
                        st.success(f"Checked in {student_name} to {target_event}!")

            if st.session_state.last_pass:
                p = st.session_state.last_pass
                st.markdown(
                    f"""
                    <div class="pass-card">
                        <div style="color:#00E5FF;font-weight:700;letter-spacing:1.5px;">FESTFLOW DIGITAL E-PASS</div>
                        <h3 style="margin:6px 0;">{p['name']}</h3>
                        <p style="margin:2px 0;color:#CBD5E1;">Reg No: <b>{p['reg']}</b> • Pass ID: <code>{p['pass_id']}</code></p>
                        <p style="margin:4px 0;color:#FFD166;">🏛️ {p['event']} ({p['venue']})</p>
                        <small style="color:#94A3B8;">Verified at {p['time']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_plan:
            st.markdown("#### 🗓️ My Personal Fest Planner & Clash Detector")
            st.caption("Pick the events you want to attend — FestFlow automatically flags overlapping timings.")
            id_to_label = {
                r["id"]: f"{r['icon']} {r['name']} ({format_hour(r['start_hour'])}–{format_hour(r['end_hour'])})"
                for _, r in df.iterrows()
            }
            chosen_ids = st.multiselect(
                "Bookmark Events",
                options=list(id_to_label.keys()),
                default=st.session_state.my_schedule,
                format_func=lambda x: id_to_label[x],
            )
            st.session_state.my_schedule = chosen_ids

            clashes = detect_clashes(chosen_ids, df)
            if clashes:
                st.error("🚨 **Schedule Clash Detected!**")
                for c in clashes:
                    st.markdown(c)
            elif chosen_ids:
                st.success("✅ Zero time clashes! Your fest itinerary is conflict-free.")

            if chosen_ids:
                plan_df = df[df["id"].isin(chosen_ids)][
                    ["icon", "name", "venue", "status", "occupancy_pct"]
                ].copy()
                plan_df.columns = ["", "Event", "Venue", "Live Status", "Crowd %"]
                st.dataframe(plan_df, width="stretch", hide_index=True)

    # -------------------------------------------------------------------------
    # TAB 4: ROLLING TROPHY LEADERBOARD & LIVE BUZZ FEED
    # -------------------------------------------------------------------------
    with tab4:
        lb_col, buzz_col = st.columns([1.3, 1])

        with lb_col:
            st.markdown("#### 🏆 Inter-Department Rolling Trophy Standings")
            lb_df = st.session_state.leaderboard_df
            fig_lb = px.bar(
                lb_df,
                x="Points",
                y="Department",
                orientation="h",
                color="Points",
                text="Points",
                color_continuous_scale="Sunsetdark",
                template="plotly_dark",
                height=360,
            )
            fig_lb.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(fig_lb, width="stretch")

        with buzz_col:
            st.markdown("#### 📡 Live Campus Buzz Feed")
            for msg in st.session_state.buzz_feed:
                st.markdown(f"> {msg}")


render_live_dashboard()
