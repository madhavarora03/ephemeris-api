# Ephemeris API
> Open Swiss Ephemeris REST API

## Download ephemeris files locally
```bash
uv run scripts/download_ephe.py
```

## Run application
### Build Docker image
```bash
docker build -t ephemeris-api .
```
### Run Image
```bash
docker run --rm -p 8000:8000 ephemeris-api:latest
```
