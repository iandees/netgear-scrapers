# netgear-scrapers
Scrapers to pull status data from Netgear R7000 routers and CM1000 cable modems and push them into InfluxDB.

## Usage

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

Install mechanize dependency
```
pip install mechanize
```

Run it.
```
python periodically.py
```
