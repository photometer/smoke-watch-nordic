FROM python:3.15-slim

# GDAL command line tools (gdalinfo, gdal_translate, ogr2ogr).
# Check HDF4 support with: gdalinfo --formats | grep HDF4
RUN apt-get update \
    && apt-get install -y --no-install-recommends gdal-bin \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /bin/

WORKDIR /opt/prefect/smoke-watch-nordic

# Install dependencies first so this layer is cached when only code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
COPY README.md ./
RUN uv sync --frozen --no-dev

ENV PATH="/opt/prefect/smoke-watch-nordic/.venv/bin:$PATH"
