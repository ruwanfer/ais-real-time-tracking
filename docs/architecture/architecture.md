# Architecture Diagram

## High-level architecture

```mermaid
flowchart LR
  A[Data Sources\nCSV / API / GeoJSON] --> B[ETL / Ingestion\nPython script / Airflow]
  B --> C[(PostgreSQL + PostGIS)]
  C --> D[Backend API\nFastAPI / Node]
  D --> E[Frontend\nWeb App + Map]
  E --> F[Map Library\nLeaflet / Mapbox / OpenLayers]
