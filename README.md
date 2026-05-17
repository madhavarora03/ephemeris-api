# Ephemeris API
> Open Swiss Ephemeris REST API

## Run application
### Build Docker image
```bash
docker build -t ephemeris-api .
```
### Run Image
```bash
docker run -p 8000:8000 -v $(pwd)/ephe:/app/ephe ephemeris-api:latest
```
