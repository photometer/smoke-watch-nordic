"""Helpers shared by the flows."""

import logging
from pathlib import Path

from prefect.futures import PrefectFuture


def collect_downloads(
    downloads: dict[str, PrefectFuture[list[Path]]], logger: logging.Logger | logging.LoggerAdapter
) -> tuple[dict[str, list[Path]], list[str]]:
    """Wait for every download, log the outcome and return (files per source, failed sources).

    A failed source is logged and skipped so the others still go through.
    """
    files: dict[str, list[Path]] = {}
    failed: list[str] = []
    for source, future in downloads.items():
        try:
            files[source] = future.result()
        except Exception:
            logger.exception("Download failed: %s", source)
            failed.append(source)
            continue
        logger.info("%s: saved %d file(s)", source, len(files[source]))
    return files, failed
