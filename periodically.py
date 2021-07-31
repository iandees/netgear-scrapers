from netgear_scrapers import CM1000Parser, R7000Parser, NestThermostat
from netgear_scrapers.influx import InfluxClient
import functools
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler


logger = logging.getLogger('scraper')
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fmt)
logger.addHandler(fh)

INFLUX_HOST = os.environ.get('INFLUX_HOST', "localhost")
INFLUX_PORT = os.environ.get('INFLUX_PORT', "8086")
INFLUX_DB = os.environ.get('INFLUX_DB', "cablemodem")
ROUTER_USER = os.environ.get('ROUTER_USER', "admin")
ROUTER_PASS = os.environ.get('ROUTER_PASS', "password")
MODEM_USER = os.environ.get('MODEM_USER', "admin")
MODEM_PASS = os.environ.get('MODEM_PASS', "password")
MODEM_AUTH = os.environ.get('MODEM_AUTH', "form")


def skip_exception(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)

    return wrapper


@skip_exception
def tick_router():
    p = R7000Parser(ROUTER_USER, ROUTER_PASS)
    data = p.fetch_data_points()
    c = InfluxClient(f"http://{INFLUX_HOST}:{INFLUX_PORT}")
    c.send_data_points(INFLUX_DB, data)


@skip_exception
def tick_modem():
    p = CM1000Parser(MODEM_USER, MODEM_PASS, MODEM_AUTH)
    data = p.fetch_data_points()
    c = InfluxClient(f"http://{INFLUX_HOST}:{INFLUX_PORT}")
    c.send_data_points(INFLUX_DB, data)


@skip_exception
def tick_nest():
    p = NestThermostat(
        os.environ.get('NEST_CLIENT_ID'),
        os.environ.get('NEST_CLIENT_SECRET'),
        os.environ.get('NEST_AUTH_CACHE')
    )
    data = p.fetch_data_points()
    c = InfluxClient(f"http://{INFLUX_HOST}:{INFLUX_PORT}")
    c.send_data_points(INFLUX_DB, data)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick_router, 'cron', second='*/10')
    scheduler.add_job(tick_modem, 'cron', minute='*')
    scheduler.add_job(tick_nest, 'cron', second='*/30')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
