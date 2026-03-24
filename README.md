markdown
# Real-Time AIS Maritime Tracking System

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Flask](https://img.shields.io/badge/Flask-2.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900?logo=leaflet&logoColor=white)](https://leafletjs.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

A production-ready real-time data engineering pipeline that processes live maritime AIS (Automatic Identification System) data from Finnish waters. The system demonstrates end-to-end data engineering capabilities including real-time ingestion, geospatial storage, WebSocket streaming, interactive visualization, and trajectory prediction.

**Data Source**: [Digitraffic.fi Marine Traffic API](https://www.digitraffic.fi/en/marine-traffic/)

## Key Features

| Feature | Implementation |
|---------|----------------|
| **Real-time Data Ingestion** | MQTT subscriber consuming 1000+ AIS messages/minute |
| **Geospatial Database** | PostgreSQL with PostGIS, 18K+ records, 377+ active vessels |
| **Live Visualization** | Leaflet.js map with 40px ship icons and COG indicators |
| **WebSocket Streaming** | Real-time updates with <3s latency |
| **Trajectory Prediction** | Linear extrapolation for 5/10/15 minute forecasts |
| **REST API** | Historical queries by vessel, time range, and prediction data |

## Architecture
Digitraffic MQTT API → collect_ais.py (Data Ingestion) → PostgreSQL + PostGIS
│
▼
WebSocket Server
│
▼
┌───────────────┴───────────────┐
│ │
▼ ▼
Leaflet Map (Browser) Prediction API (Flask)

text

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| **Data Ingestion** | Python, paho-mqtt, asyncio |
| **Database** | PostgreSQL 16, PostGIS |
| **Backend** | Flask, Flask-SocketIO, Flask-CORS |
| **Frontend** | Leaflet.js, HTML5/CSS3, WebSocket |
| **Deployment** | Docker, Git, Ubuntu/Linux |

## Database Schema

```sql
CREATE TABLE ais_ships (
    id SERIAL PRIMARY KEY,
    mmsi INTEGER,
    message_type VARCHAR(10),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    speed DECIMAL(5,2),
    course DECIMAL(5,2),
    ship_name VARCHAR(255),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
API Endpoints
Endpoint	Method	Description
/predict/<mmsi>	GET	Get 5/10/15 min trajectory predictions
/predict/random	GET	Get predictions for random active vessel
/api/vessels	GET	List all tracked vessels
/api/history/<mmsi>	GET	Query historical positions with date filters
📈 Performance Metrics
Data Processing Latency: <3 seconds

Database Records: 18,000+ positions

Active Vessels: 377+ with names and positions

Query Response Time: <200ms (indexed queries)

Concurrent Connections: Supports multiple WebSocket clients

Quick Start
Prerequisites
Python 3.8+

PostgreSQL 16+

Git

Installation
bash
# Clone repository
git clone https://github.com/ruwanfer/ais-real-time-tracking.git
cd ais-real-time-tracking

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure PostgreSQL
createdb ais_data
psql -d ais_data -c "CREATE TABLE ais_ships (
    id SERIAL PRIMARY KEY,
    mmsi INTEGER,
    message_type VARCHAR(10),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    speed DECIMAL(5,2),
    course DECIMAL(5,2),
    ship_name VARCHAR(255),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

# Start data collection (Terminal 1)
python src/collect_ais.py

# Start WebSocket server (Terminal 2)
python src/websocket_server.py

# Start prediction API (Terminal 3)
python src/prediction_api.py

# Open browser
http://localhost:5000
Project Structure
text
ais-real-time-tracking/
├── src/
│   ├── collect_ais.py          # MQTT data ingestion
│   ├── websocket_server.py     # WebSocket server
│   ├── prediction_api.py       # Trajectory prediction API
│   ├── history_api.py          # Historical data API
│   ├── map_websocket.html      # Leaflet map interface
│   ├── check_ships.py          # Database verification
│   ├── create_named_view.py    # Named ships view
│   └── setup.py                # Database initialization
├── requirements.txt
├── .gitignore
└── README.md
Screenshots
Live Map View
*Ship icons with prediction lines showing 5/10/15 minute trajectories*

Database Snapshot
*17,943 records with real-time March 2026 data*

Technical Highlights
Real-time Processing: Sub-3 second latency from data ingestion to visualization

Geospatial Optimization: PostgreSQL indexes on MMSI and timestamp for sub-200ms queries

CORS Configuration: Cross-origin resource sharing for API accessibility

Error Handling: Graceful degradation with skipped vessel tracking

Modular Design: Separation of concerns across ingestion, storage, API, and visualization

Future Enhancements
Machine learning-based trajectory prediction (LSTM models)

Historical vessel track replay

Docker containerization for one-click deployment

Vessel type classification and filtering

Real-time collision detection alerts

Export data as CSV/GeoJSON

License
This project is licensed under the MIT License.

Contact
Ruwan Gammanage
GitHub

Built as a data engineering portfolio project demonstrating real-time pipeline architecture, geospatial data processing, and interactive visualization.
