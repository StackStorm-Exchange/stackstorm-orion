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
# limitations under the License.

from lib.actions import OrionBaseAction


class NodeDiscoverAndAddInterfacesbyNameandType(OrionBaseAction):
    def run(self, node, admin_up_required, interface_names, interface_type):
        """
        Discover and add interfaces on an Orion node

        Args:
           node: Node to discover and add interfaces on.
           admin_up_required: Filter add interfaces by ifAdminStatus up or not
           interface_names: List of ifName values to filter add interfaces
           interface_type: List of ifType values to filter add interfaces

        """
        results = {'added': [], 'existing': [], 'removed': []}

        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            raise ValueError("Node not found")

        Discoverdinterfaces = self.invoke('Orion.NPM.Interfaces',
                                          'DiscoverInterfacesOnNode',
                                          orion_node.npm_id)

        add_interfaces = []
        for interface in Discoverdinterfaces['DiscoveredInterfaces']:
            # Unmonitored interfaces have an InterfaceID of 0.
            if not interface['InterfaceID'] == 0:
                self.logger.info("Skipping {} as monitored (I:{})".format(
                    interface['Caption'],
                    interface['InterfaceID']))
                results['existing'].append(
                    {interface['Caption']: interface['InterfaceID']})
            else:
                self.logger.info("Interface {} NOT monitored. (ID:{} Type:{} \
                Admin Status:{} )".format(
                    interface['Caption'],
                    interface['InterfaceID'],
                    interface['ifType'],
                    interface['ifAdminStatus']))

                # admin_up_required is defined as boolean in YAML file
                if admin_up_required:
                    # Loop through values in interface_type list, compare to Discovered interface
                    # data and add interfaces with IfType values that match what is provided in list
                    # and have the IfAdminStatus value as "UP" or 1
                    for iftype in interface_type:
                        if interface['ifAdminStatus'] == 1 and interface['ifType'] == iftype:
                            self.logger.info('Interface: {} is of IfType: {}. Adding...'.format(
                                interface['Caption'],
                                interface['ifType']))
                            add_interfaces.append(interface)
                else:
                    # Loop through values in interface_type list, compare to Discovered interface
                    # data and add interfaces with IfType values that match what is provided in list
                    # without checking the IfAdminStatus value
                    for iftype in interface_type:
                        if interface['ifType'] == iftype:
                            self.logger.info('Interface: {} is of IfType: {}. Adding...'.format(
                                interface['Caption'],
                                interface['ifType']))
                            add_interfaces.append(interface)
        self.logger.info('Adding interfaces to monitoring config...')
        additions = self.invoke('Orion.NPM.Interfaces',
                                'AddInterfacesOnNode',
                                orion_node.npm_id,
                                add_interfaces,
                                'AddDefaultPollers')

        for i in additions['DiscoveredInterfaces']:
            results['added'].append({i['Caption']: i['InterfaceID']})

        self.logger.info('Querying list of monitored interfaces from Solarwinds...')

        # Add NodeID variable info to query string
        query = 'SELECT NodeID, InterfaceID, Name, Alias, IfName, InterfaceAlias, Uri FROM ' \
                'Orion.NPM.Interfaces WHERE NodeID=' + str(orion_node.npm_id)

        # Query for the complete list of interfaces that were added to Solarwinds for monitoring
        npminterfaces = self.query(query)

        # Loop through query results and compare IfName data to interface_name list and remove
        # entries not in list
        for interface in npminterfaces['results']:
            if interface['IfName'] not in interface_names:
                self.logger.info(
                    'Interface: {} NOT included in list to be monitored.  Removing...'.format(
                        interface['IfName']))
                self.delete(interface['Uri'])
                results['removed'].append({interface['IfName']: interface['InterfaceID']})

        return results
