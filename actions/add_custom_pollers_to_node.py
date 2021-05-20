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
from lib.utils import send_user_error


class AddCustomPollersToNode(OrionBaseAction):
    def run(self, node, custompollers):
        """
        Add list of SNMP Pollers to Node

        Args:
        - node: The caption in Orion of the node to poll.
        - custompollers: The list of Orion Custom SNMP pollers to add to the Node

        Returns
        - List of custom pollers that were added to the Node, a list of Custom pollers that were
        already assigned to the Node, and a list of Custom pollers that were not found in the system

        Raises:
        - ValueError: When a node is not found.

        """
        # Create empty results dict to hold action output data
        results = {'added': [], 'existing': [], 'not_found': []}

        # Establish a connection to the Orion Server
        self.connect()

        # Find the Node in the system
        orion_node = self.get_node(node)

        if not orion_node.npm:
            error_msg = "Node not found"
            send_user_error(error_msg)
            raise ValueError(error_msg)

        # Create a query string needed to pull the custom poller data assigned to the Node
        # from the Orion DB

        self.logger.info('Querying list of custom pollers already configured on Node...')

        nodequery = 'SELECT NodeID, CustomPollerID FROM Orion.NPM.CustomPollerAssignmentOnNode ' \
                    'WHERE NodeID=' + str(orion_node.npm_id)

        # Execute the query for the custom Node pollers
        nodeassignedpollers = self.query(nodequery)

        # Create an empty list of CustomPollerIDs used to hold the ID for each of the pollers
        # passed as input to the action

        custompollerids = []

        # Loop through all the pollers provided as input to the action and query the Orion DB
        # for the CustomPollerID.

        for entry in custompollers:
            pollerquery = 'SELECT CustomPollerID, UniqueName FROM Orion.NPM.CustomPollers where ' \
                          'UniqueName=\'' + str(entry) + '\''
            entrypollerid = self.query(pollerquery)

            # Check if the Custom Poller query returned exactly 1 result as expected
            if len(entrypollerid['results']) == 1:
                # Check if Custom Poller ID is included in the list returned from the existing
                # poller query
                if any(element for element in nodeassignedpollers['results'] if
                       element['CustomPollerID'] == entrypollerid['results'][0]['CustomPollerID']):
                    self.logger.info('Custom Poller {} already assigned to Node. Skipping...'
                                     ''.format(entry))
                    # Update results data with matching poller name
                    results['existing'].append(entry['UniqueName'])
            else:
                # Add Custom Poller ID to list if not found to have already been assigned to the
                # Node
                custompollerids.append(entrypollerid['results'][0])

            # Check if the Custom poller query returned either 0 or more than the expected 1
            if len(entrypollerid['results']) >= 1 or len(entrypollerid['results']) == 0:
                self.logger.info('Custom poller {} not found in Orion DB or the text query returned'
                                 ' multiple entries and will be ignored...'.format(entry))
                results['not_found'].append(entry)

        # After validating all the pollers have not already been assigned to the Node, loop
        # through all the entries and assign them to the Node

        for entry in custompollerids:
            self.logger.info('Add Entry: {}'.format(entry))
            entrydata = {
                "NodeID": str(orion_node.npm_id),
                "CustomPollerID": entry['CustomPollerID']
            }
            response = self.create('Orion.NPM.CustomPollerAssignmentOnNode', **entrydata)
            self.logger.info('Custom poller {} successfully assigned to Node: {}'.format(
                entry['CustomPollerID'], response))
            # Update results data with matching poller name
            results['added'].append(entry['UniqueName'])
        return results

