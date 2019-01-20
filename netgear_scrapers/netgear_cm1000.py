import datetime
import re
import requests
import sys
from netgear_scrapers.influx import InfluxDataPoint, InfluxClient


class CM1000Parser(object):
    def __init__(self, username, password):
        self._auth = (username, password)

    def fetch_data_points(self):
        s = requests.Session()

        r = s.get('http://192.168.100.1/DocsisStatus.asp', auth=self._auth)
        r = s.get('http://192.168.100.1/DocsisStatus.asp', auth=self._auth)

        if r.status_code != 200:
            print("bad response: ", r.status_code, r.text)
            sys.exit(1)

        influx_points = []

        # Parse the downstream channels
        regex = r"^    <tr><td>(?P<channel>\d*)</td><td>(?P<status>[\w\s]*)</td><td>(?P<modulation>\w*)</td><td>(?P<channel_id>\d*)</td><td>(?P<frequency>\d*) Hz</td><td> ?(?P<power>[\d\.]*) dBmV</td><td> ?(?P<snr>[\d\.]*) dB</td><td>(?P<codewords_unerrored>\d*)</td><td>(?P<codewords_correctable>\d*)</td><td>(?P<codewords_uncorrectable>\d*)</td></tr>$"
        matches = re.finditer(regex, r.text, re.MULTILINE)
        for chan in matches:
            d = InfluxDataPoint("cablemodem")\
                .with_tag('direction', 'downstream')\
                .with_tag('channel', chan.group('channel'))\
                .with_field('status', chan.group('status'))\
                .with_field('modulation', chan.group('modulation'))\
                .with_field('frequency', int(chan.group('frequency')))\
                .with_field('power', float(chan.group('power')))\
                .with_field('snr', float(chan.group('snr')))\
                .with_field('codewords_unerrored', int(chan.group('codewords_unerrored')))\
                .with_field('codewords_correctable', int(chan.group('codewords_correctable')))\
                .with_field('codewords_uncorrectable', int(chan.group('codewords_uncorrectable')))
            influx_points.append(d)

        # Parse the upstream channels
        regex = r"^    <tr><td>(?P<channel>\d*)</td><td>(?P<status>[\w\s]*)</td><td>(?P<modulation>\w*)</td><td>(?P<channel_id>\d*)</td><td>(?P<frequency>\d*) Hz</td><td> ?(?P<power>[\d\.]*) dBmV</td></tr>$"
        matches = re.finditer(regex, r.text, re.MULTILINE)
        for chan in matches:
            d = InfluxDataPoint("cablemodem")\
                .with_tag('direction', 'upstream')\
                .with_tag('channel', chan.group('channel'))\
                .with_field('status', chan.group('status'))\
                .with_field('modulation', chan.group('modulation'))\
                .with_field('frequency', int(chan.group('frequency')))\
                .with_field('power', float(chan.group('power')))
            influx_points.append(d)

        return influx_points


def main():
    a = CM1000Parser('admin', 'password')
    c = InfluxClient('http://192.168.1.17:32775')

    data = a.fetch_data_points()
    c.send_data_points(data)


if __name__ == "__main__":
    main()
