import argparse
from datetime import date


def main(argv: list[str] | None = None) -> None:
    """Command line entry point (console script `smoke-watch-nordic`).

    smoke-watch-nordic daily [--day 2018-07-21]
    smoke-watch-nordic backfill --start 2018-06-01 --end 2018-08-31
    smoke-watch-nordic forecast [--run-date 2026-11-18]
    """
    parser = argparse.ArgumentParser(prog="smoke-watch-nordic")
    parser.add_argument("--domain", help="domain name from domains.yaml (default: settings)")
    commands = parser.add_subparsers(dest="command", required=True)

    daily = commands.add_parser("daily", help="observations for one day (default: yesterday)")
    daily.add_argument("--day", type=date.fromisoformat, help="UTC day, YYYY-MM-DD")

    backfill = commands.add_parser("backfill", help="observations for every day of a period")
    backfill.add_argument("--start", type=date.fromisoformat, required=True, help="YYYY-MM-DD")
    backfill.add_argument("--end", type=date.fromisoformat, required=True, help="YYYY-MM-DD")

    forecast = commands.add_parser("forecast", help="forecast for a recent run (default: today)")
    forecast.add_argument("--run-date", type=date.fromisoformat, help="UTC run date, YYYY-MM-DD")

    args = parser.parse_args(argv)

    from smoke_watch.config import load_env_files

    # Load .env.<SMOKE_ENV> before importing Prefect: it reads PREFECT_* variables on import.
    load_env_files()

    if args.command == "daily":
        from smoke_watch.flows.daily import daily_pipeline

        daily_pipeline(day=args.day, domain_name=args.domain)
    elif args.command == "backfill":
        from smoke_watch.flows.backfill import backfill as backfill_flow

        backfill_flow(start=args.start, end=args.end, domain_name=args.domain)
    else:
        from smoke_watch.flows.forecast import forecast_pipeline

        forecast_pipeline(run_date=args.run_date, domain_name=args.domain)
