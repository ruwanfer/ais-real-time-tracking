# Finnish AIS Data Engineering Pipeline

##  Description
Real-time data pipeline for processing Finnish maritime AIS data with visualization and prediction capabilities.

**Data Source**: [Digitraffic.fi Marine Traffic API](https://www.digitraffic.fi/en/marine-traffic/)

##  Current Status (Week 4 - Feb 9, 2024)
✅ **Phase 1 Complete**: Real-time AIS data collection & PostgreSQL storage  
🔄 **Phase 2 In Progress**: REST API development  
⏳ **Phase 3**: Real-time visualization  
⏳ **Phase 4**: Trajectory prediction  

##  Latest Results
- **81+ unique vessels** tracked with names
- **1000+ AIS messages** stored in database
- **Real-time processing** (<5 sec latency)
- **Complete data**: Positions, speeds, courses, ship names

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
📦 dep_26_group_13/
├── 📁 src/
│   ├── 📄 collect_ais.py     # Main data collection
│   ├── 📄 setup_ais.py       # Database setup
│   └── 📄 check_ships.py     # Verification
├── 📁 docs/
│   └── 📄 week4_progress.md  # Weekly report
├── 📁 database/
│   └── 📄 schema.sql         # Database schema
├── 📄 README.md              # Project documentation
├── 📄 requirements.txt       # Python dependencies
└── 📄 .gitignore            # Ignored files

##  Database Schema
CREATE TABLE ais_ships (
    id SERIAL PRIMARY KEY,
    mmsi INTEGER,                    -- Maritime Mobile Service Identity
    message_type VARCHAR(10),        -- 'location' or 'metadata'
    latitude DECIMAL(9,6),           -- Position (-90 to 90)
    longitude DECIMAL(9,6),          -- Position (-180 to 180)
    speed DECIMAL(5,2),              -- Speed Over Ground (knots)
    course DECIMAL(5,2),             -- Course Over Ground (degrees)
    ship_name VARCHAR(255),          -- Vessel name
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


##  Team Members
- **Ruwan Gammanage** 
- **Chandrasekara, Umesha** 
- **Aldhaher, Ola Kh. Abdulsaheb** 

##  Project Timeline
| Week | Dates | Focus | Status |
|------|-------|-------|--------|
| 3 | Jan 27-Feb 2 | Research & Planning | ✅ |
| 4 | Feb 3-9 | Database & Data Collection | ✅ |
| 5 | Feb 10-16 | REST API Development | 🔄 |
| 6 | Feb 17-23 | Real-time Visualization | ⏳ |
| 7 | Feb 24-Mar 1 | Trajectory Prediction | ⏳ |
| 8-11 | Mar 2-30 | Integration & Deployment | ⏳ |

##  Resources
- [Digitraffic API Docs](https://www.digitraffic.fi/en/marine-traffic/)
- [Full Documentation](docs/)
- [Week 4 Progress Report](docs/week4_progress.md)

---
**Repository**: https://git.dc.turkuamk.fi/ruwan.gammanage/dep_26_group_13  
**Last Updated**: February 9, 2024
