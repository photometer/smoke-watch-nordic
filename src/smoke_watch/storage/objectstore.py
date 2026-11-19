"""S3-compatible object storage access."""

from pathlib import Path


def upload_file(local_path: Path, key: str) -> None:
    """Upload a file to the configured bucket under the given key."""
    # TODO: boto3 client built from Settings.s3_endpoint_url
    raise NotImplementedError


def download_file(key: str, local_path: Path) -> Path:
    """Download an object to a local path."""
    raise NotImplementedError


def exists(key: str) -> bool:
    """Return True if the object already exists (used to skip finished work)."""
    raise NotImplementedError
