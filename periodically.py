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

influx_base = os.environ.get('INFLUX_URL')
influx_db = os.environ.get('INFLUX_DB')


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
    p = R7000Parser('admin', os.environ.get('ROUTER_PASSWORD'))
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    c.send_data_points(influx_db, data)


@skip_exception
def tick_modem():
    p = CM1000Parser('admin', os.environ.get('MODEM_PASSWORD'))
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    c.send_data_points(influx_db, data)


@skip_exception
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
