# vpp-simulator
Goal: Build a Python app that simulates a group of distributed energy resources (DERs) — like batteries, EV chargers, and solar panels — and a central controller that orchestrates them to respond to energy demand conditions. 

Stack to potentially consider:

- Simulation Engine: Pure Python so it can be simple and flexible
- Backend API: FastAPI because it is asynchronous, great for simulation-style services
- State Storage: SQLite or in-memory dict. Keeps it lightweight
- Dashboard: Streamlit or Plotly Dash for fast prototyping, interactive charts
- Task Loop: asyncio or APScheduler for time-based updates

#Dependencies:
- Dash
- Pandas