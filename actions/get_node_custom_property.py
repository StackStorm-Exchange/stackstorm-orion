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


class GetNodeCustomProperty(OrionBaseAction):
    def run(self, node, custom_property):
        """
        Gets a specific Node Custom Property.
        """
        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            msg = "Node ({}) does not exist".format(node)
            send_user_error(msg)
            raise ValueError(msg)

        swql = """SELECT {1}
        FROM Orion.NodesCustomProperties
        WHERE NodeID={0}""".format(orion_node.npm_id, custom_property)
        data = self.query(swql)

        if 'results' not in data:
            msg = "No results from Orion: {}".format(data)
            self.logger.info(msg)
            raise Exception(msg)

        if len(data['results']) == 1:
            results = data['results'][0]
            return results.get(custom_property)
        elif len(data['results']) >= 2:
            self.logger.debug(
                "Muliple Properties match '{}'".format(node))
            raise ValueError("Muliple Properties match '{}'".format(node))
