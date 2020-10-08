from orionsdk import SwisClient
from requests.exceptions import ConnectionError
from st2reactor.sensor.base import PollingSensor


class SolarwindsApiCheck(PollingSensor):
    """
    This sensor is used to fire a trigger when it detects that the API is down
    """

    def setup(self):
        server = self._config['orion_host']
        user = self._config['orion_user']
        passwd = self._config['orion_password']

        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

        self.client = SwisClient(server, user, passwd)
        self._logger.debug(self.client)

        pass

    def poll(self):
        try:
            self._logger.debug('SolarWinds API check poll')

            # We need to run a query because the connection itself will not return an error
            swql = """SELECT Name, MethodName, EntityName
            FROM Metadata.Verb where CanInvoke=@CanInvoke"""
            kargs = {'CanInvoke': True}
            orion_data = self.client.query(swql, **kargs)
            self._logger.debug("SolarWinds API query successful")
            self._logger.debug(orion_data)
        except ConnectionError:
            self._logger.debug('Dispatch SolarWinds API down trigger')
            self.sensor_service.dispatch(trigger='orion.solarwinds_api_down')

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
