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

from datetime import datetime, timedelta

from lib.actions import OrionBaseAction


class NodeUnmanage(OrionBaseAction):
    def run(self, node, minutes=None, start_date=None, end_date=None):
        """
        Unmanage an Orion node
        """

        self.connect()

        orion_node = self.get_node(node)

        if not orion_node.npm:
            raise ValueError("Node not found")

        NodeId = "N:{}".format(orion_node.npm_id)

        start_utc = None
        end_utc = None
        if minutes is not None:
            """If minutes is given get current time in UTC then add the minutes to the
            end of the time to get End time. All dates must be in UTC Format
            """
            if minutes > self.config['unmanage_max']:
            raise ValueError(
                "minutes ({}) greater than unmanage_max ({})".format(
                    minutes, self.config['unmanage_max']))

            start_utc = datetime.utcnow()
            end_utc = start_utc + timedelta(minutes=minutes)
        elif start_date is not None and end_date is not None:
            """Get the UTC offest from substracting the current Local time from the
            Current UTC time. The use that to convert the given start and end times to
            utc times so that it can be sent to SolarWinds
            """
            UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()

            start_local = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            start_utc = start_local + UTC_OFFSET_TIMEDELTA

            end_local = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
            end_utc = end_local + UTC_OFFSET_TIMEDELTA
        else:
            raise ValueError("Must supply either minutes or start_date and end_date")

        orion_data = self.invoke("Orion.Nodes",
                                 "Unmanage",
                                 NodeId,
                                 start_utc,
                                 end_utc,
                                 False)

        # This Invoke always returns None, so check and return True
        if orion_data is None:
            return True
        else:
            return orion_data
