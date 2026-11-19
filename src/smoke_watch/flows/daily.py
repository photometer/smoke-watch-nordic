"""Daily pipeline: download sources, validate, regrid, summarise per region, catalog."""

from datetime import date
from pathlib import Path

from prefect import flow, get_run_logger
from prefect.futures import PrefectFuture

from smoke_watch.config import get_settings, load_domain
from smoke_watch.dates import resolve_day
from smoke_watch.flows.common import collect_downloads

# from prefect import task
# from smoke_watch.catalog import stac_items
# from smoke_watch.domain import Domain
# from smoke_watch.processing import cog, grid, smoke_rule, validate, zonal
# from smoke_watch.sources import boundaries, firms, gdas, hysplit, modis, nilu, s5p, viirs
# from smoke_watch.storage import objectstore, paths


# Download tasks. Each one saves the raw files of one source for one day and returns their
# paths, so the flow can collect, upload and log every source the same way.


# @task(retries=3, retry_delay_seconds=60)
# def download_firms(domain: Domain, day: date, map_key: str, out_dir: Path) -> list[Path]:
#     source = "MODIS_SP"
#     csv_text = firms.fetch_firms_csv(domain, day, map_key, source=source)
#     return [firms.save_csv(csv_text, out_dir, day, source)]


# @task(retries=3, retry_delay_seconds=300)
# def download_maiac(domain: Domain, day: date, out_dir: Path) -> list[Path]:
#     granules = modis.search_maiac(domain, day, day)
#     return modis.download_granules(granules, out_dir)
#
#
# @task(retries=3, retry_delay_seconds=300)
# def download_aerdb(domain: Domain, day: date, out_dir: Path) -> list[Path]:
#     granules = viirs.search_aerdb(domain, day, day)
#     return viirs.download_granules(granules, out_dir)
#
#
# @task(retries=3, retry_delay_seconds=120, tags=["cdse"])  # tag: concurrency limit for CDSE
# def download_s5p(domain: Domain, day: date, out_dir: Path) -> list[Path]:
#     product_ids = s5p.search_s5p(domain, day)
#     return s5p.download_s5p(product_ids, out_dir)
#
#
# @task(retries=3, retry_delay_seconds=120)
# def download_nilu(day: date, out_dir: Path) -> list[Path]:
#     path = out_dir / f"nilu_pm25_{day:%Y%m%d}.parquet"
#     path.parent.mkdir(parents=True, exist_ok=True)
#     nilu.fetch_observations(day).to_parquet(path)
#     return [path]


@flow
def daily_pipeline(day: date | None = None, domain_name: str | None = None) -> None:
    """Observations for one UTC day: was there smoke over each region?

    Leave `day` empty for yesterday (the daily schedule) or set any archive date (manual runs,
    backfill). Every source here must therefore have an archive; forecast sources live in
    flows/forecast.py.
    """
    logger = get_run_logger()
    settings = get_settings()
    domain = load_domain(domain_name or settings.domain)
    day = resolve_day(day)
    # raw_dir = settings.data_dir / "raw" / domain.name / f"{day:%Y%m%d}"
    logger.info("Running %s for %s", domain.name, day)

    # 1. Start all downloads at once; they run concurrently on the flow's thread pool.
    downloads: dict[str, PrefectFuture[list[Path]]] = {
        # "firms": download_firms.submit(
        #     domain, day, settings.firms_map_key.get_secret_value(), raw_dir / "firms"
        # ),
        # "maiac": download_maiac.submit(domain, day, raw_dir / "maiac"),
        # "aerdb": download_aerdb.submit(domain, day, raw_dir / "aerdb"),
        # "s5p": download_s5p.submit(domain, day, raw_dir / "s5p"),
        # "nilu": download_nilu.submit(day, raw_dir / "nilu"),
        # TODO: CAMS analysis or reanalysis (EAC4) for this day, if the smoke rule needs it
    }

    # 2. Collect results. A failed source is skipped so the others still go through;
    #    the run is marked failed at the end.
    raw_files, failed = collect_downloads(downloads, logger)
    # for source, files in raw_files.items():
    #     for path in files:
    #         key = paths.raw_prefix(domain.name, source, day) + path.name
    #         objectstore.upload_file(path, key)

    # 3. Validate. Bad inputs go to quarantine instead of breaking the steps below.
    # fields: dict[str, xr.DataArray] = {}
    # for product, (source, variable) in PRODUCTS.items():  # e.g. "aod": ("maiac", ...)
    #     if source not in raw_files:
    #         continue
    #     da = open_field(raw_files[source], variable)  # TODO: readers for HDF4, NetCDF4, GRIB2
    #     try:
    #         validate.check_missing_fraction(da, max_missing=0.9)
    #         validate.check_value_range(da, *VALID_RANGES[product])
    #     except validate.ValidationError as err:
    #         logger.warning("%s rejected: %s", product, err)
    #         # TODO: move raw files to paths.quarantine_prefix(domain.name, source, day)
    #         continue
    #     fields[product] = da

    # 4. Regrid every field to the shared domain grid and store it as a COG.
    # bounds = grid.target_bounds(domain)
    # for product, da in fields.items():
    #     fields[product] = regrid(da, domain.crs, bounds, domain.resolution_m)  # TODO: helper
    #     key = paths.processed_key(domain.name, product, day)
    #     cog.write_cog(fields[product], settings.data_dir / key)
    #     objectstore.upload_file(settings.data_dir / key, key)

    # 5. Statistics per region (mean, p90, valid fraction) -> database.
    # region_key = paths.reference_key("boundaries", domain.region_key)
    # regions_path = objectstore.download_file(region_key, settings.data_dir / region_key)
    # regions = boundaries.load_regions(regions_path)
    # region_stats = {product: zonal.zonal_stats(da, regions) for product, da in fields.items()}
    # TODO: save region_stats to PostGIS (storage.db)

    # 6. Upwind fires: back trajectories from each region (HYSPLIT on archived GDAS winds,
    #    available for 2018 too), then fires near the trajectory points.
    # meteo = gdas.download_gdas1(day.year, day.month, settings.data_dir / "gdas")
    # TODO: per region: hysplit.write_control(...), run_hysplit(...), parse_tdump(...),
    #       then count FIRMS detections within a buffer around the trajectory points

    # 7. Smoke rule per region: combine the evidence into a smoke-day flag.
    # thresholds = smoke_rule.Thresholds(
    #     aod_p90=..., co_anomaly=..., upwind_fire_count=..., pm25_max=...
    # )
    # for region in regions.itertuples():
    #     evidence = smoke_rule.Evidence(
    #         aod_p90=..., co_anomaly=..., upwind_fire_count=..., pm25_max=...
    #     )  # None for every signal whose source failed
    #     flag = smoke_rule.is_smoke_day(evidence, thresholds)
    # TODO: save flags to PostGIS

    # 8. Catalog: one STAC item per processed product.
    # for product in fields:
    #     key = paths.processed_key(domain.name, product, day)
    #     item = stac_items.build_item(product, day, domain, f"s3://{settings.s3_bucket}/{key}")
    #     # TODO: insert item into pgSTAC

    if failed:
        raise RuntimeError(f"Sources failed: {', '.join(failed)}")


if __name__ == "__main__":
    daily_pipeline.serve(name="daily-dev", cron="0 6 * * *")
