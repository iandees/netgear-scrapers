import requests

class InfluxClient(object):
    def __init__(self, server):
        self.url = server

    def send_data_points(self, db, datapoints):
        influx_data = '\n'.join(i.as_influx_line() for i in datapoints)
        r = requests.post(self.url + '/write', params={'db': db}, data=influx_data)
        r.raise_for_status()


class InfluxDataPoint(object):
    def __init__(self, measurement, timestamp=None):
        self.measurement = measurement
        self.tag_set = {}
        self.field_set = {}
        self.timestamp = timestamp

    def with_tag(self, k, v):
        self.tag_set[k] = v
        return self

    def with_field(self, k, v):
        self.field_set[k] = v
        return self

    def as_influx_line(self):
        out = self.measurement

        if self.tag_set:
            out += "," + ",".join(k + "=" + v for k, v in sorted(self.tag_set.items(), key=lambda i: i[0]))

        out += " "

        def field_value_typer(v):
            if isinstance(v, str):
                return '"%s"' % v
            elif isinstance(v, int):
                return '%di' % v
            elif isinstance(v, bool):
                return 'true' if v == True else 'false'
            else:
                return v
        out += ",".join("%s=%s" % (k, field_value_typer(v)) for k, v in sorted(self.field_set.items(), key=lambda i: i[0]))

        if self.timestamp:
            out += " " + (self.timestamp.timestamp() * 1000 * 1000)

        return out
