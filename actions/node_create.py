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

import re

from lib.actions import OrionBaseAction
from lib.utils import send_user_error


class NodeCreate(OrionBaseAction):
    def run(self,
            node,
            ip_address,
            poller,
            mon_protocol,
            community,
            status):
        """
        Create an node in Orion.
        """
        results = {}

        results['label'] = self.connect()
        self.logger.info("Connecting to Orion: {}".format(
            results['label']))

        orion_node = self.get_node(node)
        if orion_node.npm:
            self.logger.error(
                "Node ({}) already in Orion: {}".format(orion_node,
                                                        results['label']))

            send_user_error("Node and/or IP is already in Orion!")
            raise ValueError("Node and/or IP already exists!")

        orion_ip_address = self.get_node(ip_address)
        if orion_ip_address.npm:
            self.logger.error(
                "IP ({}) already in Orion: {}".format(
                    orion_ip_address,
                    results['label']))

            send_user_error("IP is already in Orion!")
            raise ValueError("IP already exists!")

        self.logger.info(
            "Checking node ({}) is not in Orion: {}".format(
                node,
                results['label']))

        # engineID if happens to be None, default to the primary.
        if poller is not None:
            engineID = self.get_engine_id(poller)
        else:
            engineID = 1

        kargs = {'Caption': node,
                 'EngineID': engineID,
                 'IPAddress': ip_address
                 }

        if mon_protocol == "snmpv2":
            kargs['ObjectSubType'] = "SNMP"
            kargs['SNMPVersion'] = 2

        # Check if the community should be replaced.
        kargs['Community'] = self.get_snmp_community(community)

        self.logger.info("Creating Orion Node: {}".format(kargs))
        orion_data = self.create('Orion.Nodes', **kargs)

        self.logger.info("orion_data: {}".format(orion_data))

        node_id = re.search(r'(\d+)$', orion_data).group(0)
        results['node_id'] = node_id

        self.logger.info("Created Orion Node: {}".format(results['node_id']))

        pollers_to_add = {
            'N.Details.SNMP.Generic': True,
            'N.Uptime.SNMP.Generic': True,
            'N.Cpu.SNMP.HrProcessorLoad': True,
            'N.Memory.SNMP.NetSnmpReal': True,
            'N.AssetInventory.Snmp.Generic': True,
            'N.Topology_Layer3.SNMP.ipNetToMedia': True,
            'N.Routing.SNMP.Ipv4CidrRoutingTable': False
        }

        if status == 'icmp':
            pollers_to_add['N.Status.ICMP.Native'] = True
            pollers_to_add['N.Status.SNMP.Native'] = False
            pollers_to_add['N.ResponseTime.ICMP.Native'] = True
            pollers_to_add['N.ResponseTime.SNMP.Native'] = False
        elif status == 'snmp':
            pollers_to_add['N.Status.ICMP.Native'] = False
            pollers_to_add['N.Status.SNMP.Native'] = True
            pollers_to_add['N.ResponseTime.ICMP.Native'] = False
            pollers_to_add['N.ResponseTime.SNMP.Native'] = True

        pollers = []
        for p in pollers_to_add:
            pollers.append({
                'PollerType': p,
                'NetObject': 'N:{}'.format(node_id),
                'NetObjectType': 'N',
                'NetObjectID': node_id,
                'Enabled': pollers_to_add[p]
            })

        for poller in pollers:
            response = self.create('Orion.Pollers', **poller)
            self.logger.info("Added {} ({}) poller: {}".format(
                poller['PollerType'],
                poller['Enabled'],
                response))

        return results
