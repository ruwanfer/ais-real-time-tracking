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
graph TD
    A[📦 dep_26_group_13] --> B[📁 src/]
    A --> C[📁 docs/]
    A --> D[📁 database/]
    A --> E[📄 README.md]
    A --> F[📄 requirements.txt]
    A --> G[📄 .gitignore]
    
    B --> B1[📄 collect_ais.py]
    B --> B2[📄 setup_ais.py]
    B --> B3[📄 check_ships.py]
    
    C --> C1[📄 week4_progress.md]
    
    D --> D1[📄 schema.sql]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0

##  Database Schema
erDiagram
    AIS_SHIPS {
        bigint id PK "SERIAL PRIMARY KEY"
        integer mmsi "Ship identifier"
        varchar message_type "location/metadata"
        decimal latitude "Position"
        decimal longitude "Position"
        decimal speed "Knots"
        decimal course "Degrees"
        varchar ship_name "Vessel name"
        timestamp received_at "Auto timestamp"
    }
    
    note "Indexes: mmsi, received_at, location" as N1
    AIS_SHIPS }|--|| N1 : "optimized queries"

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
