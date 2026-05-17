# Ephemeris API
> Open Swiss Ephemeris REST API

## Download ephemeris files locally
```bash
uv run scripts/download_ephe.py
```

This creates the local `ephe/` directory used by the API.

## Run application using Docker (recommended)
### Build Docker image
```bash
docker build -t ephemeris-api .
```
### Run Container
```bash
docker run --rm -p 8000:8000 ephemeris-api:latest
```

## Run Locally (development)

### Install dependencies

```bash
uv sync
```

### Start application
```bash
uv run main.py
```
