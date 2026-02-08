# Map Tools Research

## Frontend Map Libraries

| Tool | Pros | Cons | Decision |
|------|------|------|----------|
| Leaflet | Simple, lightweight, free, good with GeoJSON | Limited advanced styling | Selected |
| Mapbox GL JS | Modern and visually appealing | Requires API key and licensing | Not selected |
| OpenLayers | Powerful GIS functionality | More complex to use | Not selected |

**Decision:** Leaflet was selected because it is free, easy to use, and suitable for a student project.

## Spatial Data Storage

| Tool | Pros | Cons | Decision |
|------|------|------|----------|
| PostGIS (PostgreSQL extension) | Industry standard for spatial data | Needs setup | Selected |

## Serving Map Data

| Option | Pros | Cons | Decision |
|-------|------|------|----------|
| GeoJSON via Backend API | Simple, widely supported | Heavy for very large datasets | Selected |
| GeoServer (WMS/WFS) | GIS standard services | More configuration | Optional |
