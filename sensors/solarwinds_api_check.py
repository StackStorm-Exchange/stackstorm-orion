from orionsdk import SwisClient
from requests.exceptions import ConnectionError
from st2reactor.sensor.base import PollingSensor


class SolarwindsApiCheck(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            - get_logger() - returns logger instance specific to this sensor.
            - dispatch() for dispatching triggers into the system.
    * self._config
        - contains parsed configuration that was specified as
          config.yaml in the pack.
    """

    def setup(self):
        # Setup stuff goes here. For example, you might establish connections
        # to external system once and reuse it. This is called only once by the system.
        server = self._config['orion_host']
        user = self._config['orion_user']
        passwd = self._config['orion_password']

        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)

        self.client = SwisClient(server, user, passwd)
        self._logger.debug(self.client)

        pass

    def poll(self):
        # This is where the crux of the sensor work goes.
        # This is called every self._poll_interval.
        # For example, let's assume you want to query ec2 and get
        # health information about your instances:
        #   some_data = aws_client.get('')
        #   payload = self._to_payload(some_data)
        #   # _to_triggers is something you'd write to convert the data format you have
        #   # into a standard python dictionary. This should follow the payload schema
        #   # registered for the trigger.
        #   self.sensor_service.dispatch(trigger, payload)
        #   # You can refer to the trigger as dict
        #   # { "name": ${trigger_name}, "pack": ${trigger_pack} }
        #   # or just simply by reference as string.
        #   # i.e. dispatch(${trigger_pack}.${trigger_name}, payload)
        #   # E.g.: dispatch('examples.foo_sensor', {'k1': 'stuff', 'k2': 'foo'})
        #   # trace_tag is a tag you would like to associate with the dispatched TriggerInstance
        #   # Typically the trace_tag is unique and a reference to an external event.
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
            self._logger.debug('Dispatch SolarWinds services restart trigger')
            self.sensor_service.dispatch(trigger='orion.solarwinds_restart')

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform cleanup operations like
        # closing the connections to external system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass
