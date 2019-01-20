from netgear_scrapers import CM1000Parser, R7000Parser
from netgear_scrapers.influx import InfluxClient
import os

from apscheduler.schedulers.blocking import BlockingScheduler


influx_base = os.environ.get('INFLUX_URL')
influx_db = os.environ.get('INFLUX_DB')
router_pass = os.environ.get('ROUTER_PASSWORD')
modem_pass = os.environ.get('MODEM_PASSWORD')


def tick_router():
    p = R7000Parser('admin', router_pass)
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    print("Sending %d datapoints from the router to influx" % len(data))
    c.send_data_points(influx_db, data)


def tick_modem():
    p = CM1000Parser('admin', modem_pass)
    data = p.fetch_data_points()
    c = InfluxClient(influx_base)
    print("Sending %d datapoints from the modem to influx" % len(data))
    c.send_data_points(influx_db, data)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick_router, 'cron', second='*/10')
    scheduler.add_job(tick_modem, 'cron', minute='*')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
