# Project Plan: Finnish AIS Data Pipeline (Group 13)

**Goal:** Real-time system to collect, store, and visualize maritime AIS data.
**Deadline:** March 20, 2026

## Phase 1: Data Collection (Completed)
* **Done:** Set up PostgreSQL database with PostGIS.
* **Done:** Created Python script (`collect_ais.py`) to fetch data from Digitraffic.
* **Result:** Successfully storing 81+ vessels in the database.

## Phase 2: API Development (Due: Feb 16)
* **Goal:** Create REST API to query data.
* **Tools:** Python, FastAPI.
* **Tasks:**
    1.  Create endpoint `/ships` to list all tracked vessels.
    2.  Create endpoint `/history/{mmsi}` to see specific ship history.

## Phase 3: Map Visualization (Due: Mar 1)
* **Goal:** Show ships moving on a map in real-time.
* **Tools:** Leaflet.js (JavaScript) and WebSockets.
* **Tasks:**
    1.  Draw Baltic Sea map on a webpage.
    2.  Place markers for ships from DB.
    3.  Update positions automatically (minimal delay).

## Phase 4: Predictions & Documentation (Due: Mar 20)
* **Goal:** Predict ship paths and document system.
* **Tasks:**
    1.  Calculate predicted path based on speed/course.
    2.  Finish Architecture Diagram and Deployment Manual.