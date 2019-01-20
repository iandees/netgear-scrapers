import datetime
import re
import requests
import sys
from netgear_scrapers.influx import InfluxDataPoint

def uptime_to_seconds(uptime_str):
    if uptime_str == '--':
        return 0

    regex = r"(.+(?P<days>\d) days )?(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})"
    matches = re.match(regex, uptime_str)

    if not matches:
        return None

    delta = datetime.timedelta(
        days=int(matches.group('days')),
        hours=int(matches.group('hours')),
        minutes=int(matches.group('minutes')),
        seconds=int(matches.group('seconds')),
    )

    return int(delta.total_seconds())


class R7000Parser(object):
    def __init__(self, username, password):
        self._auth = (username, password)

    def fetch_data_points(self):
        # Use a session to store the XSRF cookie
        s = requests.Session()

        # Login once to get the XSRF
        r = s.get('http://192.168.1.1/RST_stattbl.htm', auth=self._auth)

        # Login again to get the actual data
        r = s.get('http://192.168.1.1/RST_stattbl.htm', auth=self._auth)
        if r.status_code != 200:
            print("bad response: ", r.status_code, r.text)
            sys.exit(1)

        regex = r"class=\"(thead|ttext)\">(.*)<\/span>"
        matches = re.findall(regex, r.text, re.MULTILINE)
        matches = [a[1] for a in matches]

        headers = matches[0:8]

        wan = InfluxDataPoint("router")\
            .with_tag('port', 'wan')\
            .with_field('status', matches[9])\
            .with_field('tx_pkts', int(matches[10]))\
            .with_field('rx_pkts', int(matches[11]))\
            .with_field('collisions', int(matches[12]))\
            .with_field('tx_bps', int(matches[13]))\
            .with_field('rx_bps', int(matches[14]))\
            .with_field('uptime', uptime_to_seconds(matches[15]))
        lan = InfluxDataPoint("router")\
            .with_tag('port', 'lan')\
            .with_field('tx_pkts', int(matches[18]))\
            .with_field('rx_pkts', int(matches[19]))\
            .with_field('collisions', int(matches[20]))\
            .with_field('tx_bps', int(matches[21]))\
            .with_field('rx_bps', int(matches[22]))
        lan1 = InfluxDataPoint("router")\
            .with_tag('port', 'lan1')\
            .with_field('status', matches[17])\
            .with_field('uptime', uptime_to_seconds(matches[23]))
        lan2 = InfluxDataPoint("router")\
            .with_tag('port', 'lan2')\
            .with_field('status', matches[25])\
            .with_field('uptime', uptime_to_seconds(matches[26]))
        lan3 = InfluxDataPoint("router")\
            .with_tag('port', 'lan3')\
            .with_field('status', matches[28])\
            .with_field('uptime', uptime_to_seconds(matches[29]))
        lan4 = InfluxDataPoint("router")\
            .with_tag('port', 'lan4')\
            .with_field('status', matches[31])\
            .with_field('uptime', uptime_to_seconds(matches[32]))
        wlan24 = InfluxDataPoint("router")\
            .with_tag('port', 'wlan24')\
            .with_field('status', matches[42])\
            .with_field('tx_pkts', int(matches[43]))\
            .with_field('rx_pkts', int(matches[44]))\
            .with_field('collisions', int(matches[45]))\
            .with_field('tx_bps', int(matches[46]))\
            .with_field('rx_bps', int(matches[47]))\
            .with_field('uptime', uptime_to_seconds(matches[48]))
        wlan5 = InfluxDataPoint("router")\
            .with_tag('port', 'wlan5')\
            .with_field('status', matches[50])\
            .with_field('tx_pkts', int(matches[51]))\
            .with_field('rx_pkts', int(matches[52]))\
            .with_field('collisions', int(matches[53]))\
            .with_field('tx_bps', int(matches[54]))\
            .with_field('rx_bps', int(matches[55]))\
            .with_field('uptime', uptime_to_seconds(matches[56]))

        return [wan, lan, lan1, lan2, lan3, lan4, wlan24, wlan5]
