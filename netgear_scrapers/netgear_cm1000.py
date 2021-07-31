import datetime
import re
import requests
import mechanize
import sys
from netgear_scrapers.influx import InfluxDataPoint, InfluxClient


class CM1000Parser(object):
    def __init__(self, username, password, modemauth):
        self._auth = (username, password)
        self.username = username
        self.password = password
        self.modemauth = modemauth

    def fetch_data_points(self):
        if self.modemauth == "basic":
            s = requests.Session()

            r = s.get('http://192.168.100.1/DocsisStatus.asp', auth=self._auth)
            r = s.get('http://192.168.100.1/DocsisStatus.asp', auth=self._auth)

            if r.status_code != 200:
                print("bad response: ", r.status_code, r.text)
                sys.exit(1)
            data = r.text
        elif self.modemauth == "form":
            # Use mechanise to connect, fill login form, and grab the DocsisStatus page.
            br = mechanize.Browser()
            br.set_handle_robots(False)

            try:
                br.open("http://192.168.100.1/GenieLogin.asp")
            except:
                print("Unable to connect...Exiting.")
                sys.exit(1)

            br.select_form(name="login")
            br['loginUsername'] = self.username
            br['loginPassword'] = self.password
            response = br.submit()

            for link in br.links(url_regex="DocsisStatus"):
                response1 = br.follow_link(link)

            data = response1.read().decode("utf-8")
        else:
            print("You need to set the MODEM_AUTH environment variable to either 'basic' or 'form'.")
            sys.exit(1)

        influx_points = []

        # Parse the downstream channels
        regex = r"^    <tr><td>(?P<channel>\d*)</td><td>(?P<status>[\w\s]*)</td><td>(?P<modulation>\w*)</td><td>(?P<channel_id>\d*)</td><td>(?P<frequency>\d*) Hz</td><td> ?(?P<power>[\d\.]*) dBmV</td><td> ?(?P<snr>[\d\.]*) dB</td><td>(?P<codewords_unerrored>\d*)</td><td>(?P<codewords_correctable>\d*)</td><td>(?P<codewords_uncorrectable>\d*)</td></tr>$"
        matches = re.finditer(regex, data, re.MULTILINE)
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
        matches = re.finditer(regex, data, re.MULTILINE)
        for chan in matches:
            d = InfluxDataPoint("cablemodem")\
                .with_tag('direction', 'upstream')\
                .with_tag('channel', chan.group('channel'))\
                .with_field('status', chan.group('status'))\
                .with_field('modulation', chan.group('modulation'))\
                .with_field('frequency', int(chan.group('frequency')))\
                .with_field('power', float(chan.group('power')))
            influx_points.append(d)

        #print(influx_points)
        return influx_points


def main():
    # This function isn't really used.
    a = CM1000Parser(MODEM_USER, MODEM_PASS, MODEM_AUTH)
    c = InfluxClient(f"http://{INFLUX_HOST}:{INFLUX_PORT}")

    data = a.fetch_data_points()
    c.send_data_points(data)


if __name__ == "__main__":
    main()
