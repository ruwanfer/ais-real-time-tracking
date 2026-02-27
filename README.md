# Finnish AIS Data Engineering Pipeline

##  Description
Real-time data pipeline for processing Finnish maritime AIS data with visualization and prediction capabilities.

**Data Source**: [Digitraffic.fi Marine Traffic API](https://www.digitraffic.fi/en/marine-traffic/)

##  Current Status (Week 4 - Feb 9, 2024)
✅ **Phase 1 Complete**: Real-time AIS data collection & PostgreSQL storage  
✅ **Phase 2 Complete**: WebSocket server & real-time map visualization  
🔄 **Phase 3 In Progress**: Prediction API development  
⏳ **Phase 4**: REST API for historical data 

##  Latest Results
- **124+ unique vessels** tracked with names
- **66+ active ships** on real-time map
- **Real-time processing** (<3 sec latency)
- **Complete data**: Positions, speeds, courses, ship names
- **Prediction API**: Trajectory predictions for vessel tracking

##  Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Git

### Installation
\\\ash
# Clone repository
git clone https://git.dc.turkuamk.fi/ruwan.gammanage/dep_26_group_13.git
cd dep_26_group_13

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb ais_data
python src/setup_ais.py

# Run data collection
python src/collect_ais.py
\\\

### Verify Installation
\\\ash
# Check collected ships
python src/check_ships.py
# Expected: Shows 81+ ships with names
\\\

##  Project Structure
dep_26_group_13/
├── 📁 src/
│ ├── 📄 collect_ais.py # Main data collection
│ ├── 📄 websocket_server.py # Real-time WebSocket server
│ ├── 📄 prediction_api.py # Prediction API (Week 5)
│ ├── 📄 map_websocket.html # Leaflet map visualization
│ ├── 📄 check_ships.py # Verification
│ ├── 📄 create_named_view.py # Named ships view
│ ├── 📄 setup.py # Database setup
│ └── 📄 setup_ais.py # AIS table setup
├── 📁 docs/
│ └── 📄 architecture.md # System architecture
├── 📄 README.md # Project documentation
├── 📄 requirements.txt # Python dependencies
└── 📄 .gitignore # Ignored files

##  Database Schema
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

-- View for named ships only
CREATE VIEW named_ships_only AS 
SELECT * FROM ais_ships 
WHERE ship_name IS NOT NULL;


API Endpoints
Endpoint	Description	Example
/predict/<mmsi>	Get predictions for specific ship	/predict/210607000
/predict/random	Get predictions for random ship	/predict/random


##  Team Members
- **Ruwan Gammanage** 
- **Chandrasekara, Umesha** 
- **Aldhaher, Ola Kh. Abdulsaheb** 

##  Project Timeline
| Week | Dates | Focus | Status |
|------|-------|-------|--------|
2	Feb 4-10	Research & Planning	✅
3	Feb 11-17	Database & Data Collection	✅
4	Feb 18-24	Real-time WebSocket & Map	✅
5	Feb 25-Mar 3 Prediction API	🔄
6	Mar 4-10	REST API Development	⏳
7	Mar 11-17	Enhancements	⏳
8-9	Mar 18-29	Testing & Deployment	⏳

##  Resources
- [Digitraffic API Docs](https://www.digitraffic.fi/en/marine-traffic/)
- [Full Documentation](docs/)
- [Week 4 Progress Report](docs/week4_progress.md)

---
**Repository**: https://git.dc.turkuamk.fi/ruwan.gammanage/dep_26_group_13  
**Last Updated**: February 27, 2024
