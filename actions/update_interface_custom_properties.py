# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from lib.actions import OrionBaseAction
from lib.utils import send_user_error


class UpdateInterfaceCustomProperties(OrionBaseAction):
    def run(self, node, interface, custom_property, value):
        """
        Update the Custom Properties of an Interface on a Node in Solarwinds.

        Args:
            node: Name of the Node to apply the changes to
            interface: Name of the interface to be updated
            custom_property: Name of the interface custom property to be updated
            value: The new value to apply to the interface custom property

        """
        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            msg = "Node ({}) does not exist".format(node)
            send_user_error(msg)
            raise ValueError(msg)

        query = 'SELECT Uri FROM Orion.NPM.Interfaces WHERE NodeID=' \
                + str(orion_node.npm_id) + 'AND IfName=' + interface

        interface_uri = self.query(query)

        if not interface_uri['results']:
            msg = "Interface ({}) does not exist".format(interface)
            send_user_error(msg)
            raise ValueError(msg)

        if len(interface_uri['results']) > 1:
            msg = "Interface ({}) matches multiple entries on Node: {}".format(interface, node)
            send_user_error(msg)
            raise ValueError(msg)

        current_properties = self.read(interface_uri['results'][0]['Uri']+ '/CustomProperties')

        if custom_property not in current_properties:
            msg = "Custom property {} does not exist!".format(custom_property)
            send_user_error(msg)
            raise ValueError(msg)

        kargs = {custom_property: value}

        self.logger.info('Updating Node: {} (Interface: {} Customer Property: {} Value: {})'.format(node, interface, custom_property, value))
        orion_data = self.update(interface_uri['results'][0]['Uri'] + '/CustomProperties', **kargs)

        # This update returns None, so check just in case.
        # This happens even if the custom_property does not exist!
        if orion_data is None:
            return True
        else:
            return orion_data
