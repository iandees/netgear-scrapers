# netgear-scrapers
Scrapers to pull status data from Netgear R7000 routers and CM1000 cable modems and push them into InfluxDB.

## Usage (CLI)

1. Set the following environmental variables:

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

1. Install dependencies

    ```
    pipenv install --dev --deploy --system
    ```

1. Run it.

    ```
    python periodically.py
    ```

## Usage (Docker)

1. Build it.

    ```shell
    docker build -t <username>/netgear-scrapers .
    ```

1. Edit the `docker-compose.yml` file with your local details. Make sure to adjust the image name for whatever you build it as above.

1. Run it.

    ```shell
    docker-compose up -d
    ```
