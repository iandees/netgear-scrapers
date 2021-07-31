# netgear-scrapers
Scrapers to pull status data from Netgear R7000 routers and CM1000 cable modems and push them into InfluxDB.

## Usage (CLI)

Set the following environmental variables:
```
INFLUX_HOST
INFLUX_PORT
INFLUX_DB
ROUTER_USER
ROUTER_PASS
MODEM_USER
MODEM_PASS
MODEM_AUTH (either 'basic'(older firmware) or 'form'(newer firmware))
NEST_CLIENT_ID
NEST_CLIENT_SECRET
NEST_AUTH_CACHE
```

Install dependencies
```
pipenv install --dev --deploy --system
```

Run it.
```
python periodically.py
```

## Usage (Docker)
Build it.
```shell
docker build -t <username>/netgear-scrapers.
```
Edit the `docker-compose.yml` file with your local details.
Make sure to adjust the image name for whatever you build it as above.
Run it.
```shell
docker-compose up -d
```