from netgear_scrapers import CM1000Parser, R7000Parser, NestThermostat
from netgear_scrapers.influx import InfluxClient
import os

from apscheduler.schedulers.blocking import BlockingScheduler


influx_base = os.environ.get('INFLUX_URL')
influx_db = os.environ.get('INFLUX_DB')


def tick_router():
    p = R7000Parser('admin', os.environ.get('ROUTER_PASSWORD'))
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    c.send_data_points(influx_db, data)


def tick_modem():
    p = CM1000Parser('admin', os.environ.get('MODEM_PASSWORD'))
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    c.send_data_points(influx_db, data)


def tick_nest():
    p = NestThermostat(
        os.environ.get('NEST_CLIENT_ID'),
        os.environ.get('NEST_CLIENT_SECRET'),
        os.environ.get('NEST_AUTH_CACHE')
    )
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    c.send_data_points(influx_db, data)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick_router, 'cron', second='*/10')
    scheduler.add_job(tick_modem, 'cron', minute='*')
    scheduler.add_job(tick_nest, 'cron', second='*/30')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
