# 🎪 FestFlow: Real-Time Campus Event Dashboard

**Course:** 2 MCA B — Python Programming (MCA411-2) | Component 3 Assignment  
**Institution:** CHRIST (Deemed to be University), Central Campus, Bangalore

## Overview
**FestFlow** is an interactive, real-time smart event command center built with **Python**, **Streamlit**, **Plotly 3D**, **Pandas**, and **NumPy** for managing and exploring campus fests (*Gateways, Blossoms, Darpan, In-Bloom, NextWave, Eklavya*).

## Key Features
- **Real-Time Auto-Streaming Engine:** Uses `@st.fragment(run_every=3)` to stream live crowd footfall, venue vibe scores, acoustic levels, and Rolling Trophy updates without full-page reloads.
- **Time-Based Dynamic Event Feed & Fest Clock Simulator:** Automatically classifies events as `LIVE NOW`, `STARTING SOON`, `UPCOMING`, or `COMPLETED`, with an interactive timeline Gantt chart and a time-travel slider for live demos.
- **3D Interactive Visualizations:**
  - **3D Campus Crowd Density Terrain:** Gaussian heatmap surface mapped over Central Campus venue coordinates.
  - **3D Multi-Metric Scatter Plot:** Compares Occupancy %, Acoustic Energy (dB), and Vibe Score simultaneously.
- **Live Check-In Desk & Digital E-Pass:** Simulates gate check-ins, generates a verified E-Pass, and updates campus crowd metrics immediately.
- **Personal Fest Planner & Clash Detector:** Flags overlapping event timings automatically.
- **Smart Crowd-Overflow Alerts:** Recommends alternative low-congestion venues when any auditorium exceeds 85% capacity.

## Quick Start (Local)
```bash
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deployment
Push this repository to GitHub and deploy directly on [Streamlit Community Cloud](https://share.streamlit.io) with `app.py` as the main file path.
