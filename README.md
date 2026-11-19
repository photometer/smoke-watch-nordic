# Smoke Watch Nordic

A data pipeline that answers one question every morning: **was there wildfire smoke over the regions of Norway yesterday, where did it come from, and what is expected in the next three days?**

It combines satellite products, atmospheric model output and ground stations, brings them onto one grid, summarises them per county (fylke) and flags smoke days. The same pipeline reprocesses any archive period, with the 2018 Nordic fire season as the main case study.

> **Status: work in progress.** The project structure, configuration and orchestration are in place. Data sources and processing steps are scaffolded and being implemented stage by stage (see [Roadmap](#roadmap)).

## Architecture

```
Sources ──► Prefect flows ──► Object storage (S3) ──► PostGIS ──► STAC catalogue
            extract → validate → transform → load → analyse → catalogue
```

Data is organised in layers:

| Layer | Location | Contents |
| --- | --- | --- |
| Raw | `raw/<domain>/<source>/<yyyy>/<mm>/<dd>/` | files exactly as delivered by the provider |
| Quarantine | `quarantine/...` | raw files that failed validation |
| Processed | `processed/<domain>/<product>/...` | Cloud Optimized GeoTIFFs on a common grid (EPSG:3035, 5 km) |
| Analytics | PostGIS tables | zonal statistics per county, smoke-day flags |

Keeping raw data makes every result reproducible and lets the history be reprocessed when an algorithm changes, without downloading again.

### Two flows

| Flow | Question | Sources | Dates |
| --- | --- | --- | --- |
| `daily_pipeline(day)` | Was there smoke on day X? | NASA FIRMS, MODIS MAIAC, VIIRS Deep Blue, Sentinel-5P TROPOMI, NILU stations, GDAS winds for HYSPLIT back-trajectories | any past day: scheduled for yesterday, or an archive date |
| `forecast_pipeline(run_date)` | What is expected in the next 3 days? | CAMS forecast, ECMWF Open Data | recent runs only |

`backfill(start, end)` runs the observations flow for every day of a period, e.g. summer 2018.

## Data sources

| Data | Provider | Format |
| --- | --- | --- |
| Active fires | NASA FIRMS | CSV |
| Aerosol optical depth (MCD19A2) | NASA Earthdata | HDF4 |
| Aerosol (Deep Blue, NOAA-20) | NASA Earthdata | NetCDF4 |
| CO and aerosol index | Copernicus Data Space (Sentinel-5P) | NetCDF4 |
| Aerosol and PM2.5 forecast | CAMS, Atmosphere Data Store | GRIB |
| Wind forecast | ECMWF Open Data (IFS) | GRIB2 |
| Archive winds for trajectories | NOAA ARL (GDAS1) | ARL binary |
| PM2.5 at stations | NILU | JSON |
| County boundaries | Kartverket / Geonorge | Shapefile → GeoParquet |

## Tech stack

Python 3.15 · uv · Prefect 3 · xarray, rioxarray, rasterio, GDAL · PostgreSQL + PostGIS · SQLAlchemy + Alembic · S3-compatible storage (SeaweedFS locally) · STAC · Docker · pytest, ruff, mypy

## Quick start

Requirements: [uv](https://docs.astral.sh/uv/) and Docker.

```bash
uv sync                      # install dependencies
uv run poe up                # start PostGIS, SeaweedFS and the Prefect server
uv run poe migrate           # create the database schema
uv run poe daily             # observations for yesterday
uv run poe daily --day 2018-07-21
uv run poe backfill --start 2018-06-01 --end 2018-08-31
```

The Prefect UI is at http://localhost:4200.

### Configuration

Settings are read from `SMOKE_*` environment variables. The environment is selected with `SMOKE_ENV`:

- `.env.dev` holds shared development settings without secrets and is committed.
- `.env.dev.local` holds personal API keys (FIRMS, Copernicus Data Space, Earthdata, CDS) and is git-ignored.
- In production no files are used: values come from the Prefect work pool and Secret blocks.

Required keys are listed at the end of `.env.dev`.

## Development

```bash
uv run poe test              # unit tests
uv run poe test-integration  # integration tests (needs `poe up`)
uv run poe lint              # ruff, formatting check, mypy
```

## Project layout

```
src/smoke_watch/
  config.py        settings and environment selection
  domain.py        analysis domain and bounding-box formats for each API
  dates.py         UTC day handling for daily runs and backfills
  flows/           Prefect flows: daily, backfill, forecast
  sources/         one module per data provider
  processing/      validation, regridding, COG writing, zonal statistics, smoke rule
  storage/         object storage, database, storage key layout
  catalog/         STAC items
alembic/           database migrations
tests/             unit and integration tests
```

## Roadmap

1. Skeleton, configuration, orchestration (done)
2. Vector data and SQL: FIRMS fire ingestion into PostGIS, county boundaries, NILU stations, analytical views
3. Satellite rasters: MAIAC (HDF4) and Sentinel-5P (NetCDF) on a common grid, validation and quarantine, zonal statistics, smoke-day rule, 2018 backfill
4. Catalogue and metadata: pgSTAC, stac-fastapi, STAC Browser, CF and ACDD attributes
5. Operations: CI/CD, alerts, data freshness checks, runbook
6. Burn scars from Sentinel-2 and a written report on the 2018 season

## License

MIT
