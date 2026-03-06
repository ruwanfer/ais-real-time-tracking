# Prediction Algorithm Documentation

## Overview
The Prediction API provides simple future position estimates for ships using AIS data stored in a PostgreSQL database.

The API retrieves the latest known position of a vessel and generates estimated positions for the next 5, 10, and 15 minutes. This prediction model is simple and is mainly used to demonstrate the functionality of the API and the AIS data pipeline.

---

## Data Source

The prediction system reads ship data from the PostgreSQL database.

Database used:
ais_data

The system queries the following view:

named_ships_only

This view contains ships that have valid names and position data.

The query retrieves:

- ship_name
- latitude
- longitude

Example SQL query used in the API:

SELECT ship_name, latitude, longitude
FROM named_ships_only
WHERE mmsi = %s AND latitude IS NOT NULL
ORDER BY received_at DESC
LIMIT 1

This query returns the latest known position of the ship.

---

## Prediction Process

The prediction process follows these steps.

### 1. API Request

The client sends a request to the prediction API endpoint:

/predict/<mmsi>

Example:

/predict/210607000

### 2. Retrieve Ship Position

The API connects to the PostgreSQL database and retrieves the latest position of the ship using the MMSI identifier.

### 3. Convert Data

The latitude and longitude values retrieved from the database are converted from Decimal to float values.

### 4. Generate Predictions

The system generates predicted ship positions by adding small offsets to the current coordinates.

Example calculation:

lat + 0.01  
lon + 0.01

Three future positions are generated:

- 5 minutes ahead
- 10 minutes ahead
- 15 minutes ahead

Example predicted coordinates:

| Time Ahead | Latitude | Longitude |
|------------|----------|-----------|
| 5 minutes  | lat + 0.01 | lon + 0.01 |
| 10 minutes | lat + 0.02 | lon + 0.02 |
| 15 minutes | lat + 0.03 | lon + 0.03 |

---

## API Response

The API returns a JSON response containing:

- ship name
- MMSI number
- current ship position
- predicted future positions

Example response:

{
 "ship": "Example Ship",
 "mmsi": 210607000,
 "current": {
   "lat": 60.12,
   "lon": 21.45
 },
 "predictions": [
   {"lat": 60.13, "lon": 21.46, "minutes": 5},
   {"lat": 60.14, "lon": 21.47, "minutes": 10},
   {"lat": 60.15, "lon": 21.48, "minutes": 15}
 ]
}

---

## Additional Endpoint

The API also provides another endpoint:

/predict/random

This endpoint selects a random ship with valid position data and returns predictions for that ship.

---

## Limitations

This is a simplified prediction model.

Current limitations include:

- Ship speed is not used in prediction
- Ship direction (course) is not considered
- Environmental conditions are ignored
- Predictions are approximate