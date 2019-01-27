import nest
from netgear_scrapers.influx import InfluxDataPoint


class NestThermostat(object):
    def __init__(self, client_id, client_secret, access_token_cache_file):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_cache_file = access_token_cache_file

    def fetch_data_points(self):
        with nest.Nest(client_id=self.client_id,
                       client_secret=self.client_secret,
                       access_token_cache_file=self.access_token_cache_file) as napi:
            thermostat = napi.thermostats[0]

            n = InfluxDataPoint("thermostat")\
                .with_tag('device_id', thermostat.device_id)\
                .with_field('mode', thermostat.mode)\
                .with_field('hvac_state', thermostat.hvac_state)\
                .with_field('fan', thermostat.fan)\
                .with_field('fan_timer', thermostat.fan_timer)\
                .with_field('temperature', thermostat.temperature)\
                .with_field('humidity', thermostat.humidity)\
                .with_field('target', thermostat.target)\
                .with_field('online', thermostat.online)

        return [n]
